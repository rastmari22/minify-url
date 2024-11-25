import Api from './tap/src/api';

const database = () => new Promise((resolve, reject) => {
    const req = indexedDB.open('messages', 3);
    req.onupgradeneeded = (e) => {
        const db = req.result;
        if (e.oldVersion < 1) {
            db.createObjectStore('replies', {
                keyPath: 'id',
            });
        }
        if (e.oldVersion < 2) {
            db.createObjectStore('ticket', {
                keyPath: 'id',
            });
            db.createObjectStore('tickets', {
                keyPath: 'id',
            });
        }
        if (e.oldVersion < 3) {
            db.createObjectStore('drafts', {
                keyPath: 'id',
            });
        }
    };
    req.onsuccess = () => {
        const db = req.result;
        resolve(db);
    };
    req.onerror = (e) => {
        reject(e);
    };
});

export default class TtsApi extends Api {
    constructor() {
        super();
        this.autologin = false;
        this.store.permission = undefined;
        this.store.tickets = [];
        this.store.archive = undefined;
        this.store.replies = undefined;
        this.messages = {};
        this.observers = {};
        this.visited = {};
        this.registerServiceWorkers();
    }

    get pooling() {
        return this.store.active_pooling || this.store.archive_pooling;
    }

    async pool() {
        if (this.authorized) {
            if (!this.store.active_pooling) {
                this.store.active_pooling = true;
                try {
                    const tickets = Object.keys(this.messages);
                    for (let i = 0; i < tickets.length; i += 1) {
                        this.get_ticket(tickets[i]);
                    }
                    if (this.permission > 10) {
                        const db = await database();
                        const transaction = db.transaction('tickets', 'readonly');
                        const store = transaction.objectStore('tickets');
                        const objects = await TtsApi.getAllObjects(store);
                        let ids = Object.keys(objects);
                        let reply = 0;
                        for (let i = 0; i < ids.length; i += 1) {
                            const ticket = objects[ids[i]];
                            const creply = ticket.reply;
                            if (creply.id > reply) {
                                reply = creply.id;
                            }
                        }
                        const data = await this.get_json(`/tickets?reply=${reply}`);
                        for (let i = 0; i < data.tickets.length; i += 1) {
                            const ticket = data.tickets[i];
                            const ntransaction = db.transaction('tickets', 'readwrite');
                            const nstore = ntransaction.objectStore('tickets');
                            nstore.put(ticket);
                            objects[ticket.id] = ticket;
                        }
                        const active = [];
                        const archive = [];
                        ids = Object.keys(objects);
                        for (let i = 0; i < ids.length; i += 1) {
                            const ticket = objects[ids[i]];
                            if (ticket.closed) {
                                archive.push(ticket);
                            } else {
                                active.push(ticket);
                            }
                        }
                        this.store.tickets = active.sort((a, b) => (a.reply.id > b.reply.id ? -1 : 1));
                        this.store.archive = archive.sort((a, b) => (a.reply.id > b.reply.id ? -1 : 1));
                    } else {
                        this.store.archive = undefined;
                        const data = await this.get_json('/tickets');
                        this.store.tickets = data.tickets.sort((a, b) => (a.reply.id > b.reply.id ? -1 : 1));
                    }
                } finally {
                    delete this.store.active_pooling;
                }
            }
        }
    }

