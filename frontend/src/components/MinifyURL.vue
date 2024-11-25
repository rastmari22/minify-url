<template>
    <div class="link-input-contsiner">
        <input v-model="url" placeholder="Вставьте ссылку"/>
        <button @click="sendLink()">Сократить</button>
        <p v-if="msg">{{ msg }}</p>
        <p v-if="short_url">
            Новая ссылка: <a :href="short_url">{{ short_url }}</a>
        </p>
        
    </div>
</template>

<script>
    export default {
        name: 'MinifyURL',
        data() {
            return {
                url: '',
                msg: '',
                short_url:'',
                go_to:''                
            }
        },
        methods: {
            async getLink(short_url) {
                const response = await fetch(`${short_url}`, {
                    method: 'GET'
                })
                const data = await response.json()
                if (data.long_url) {
                    this.short_url = data.long_url
                } 
            },
            async sendLink() {

                let urlToServer = {
                    url: this.url
                }

                const userData = {
                    'username': 'user2',
                    'password': '111'
                }

                const response = await fetch('http://localhost:5000/short', {
                    method: 'POST',
                    headers: {
                        'Authorization': `Basic ${btoa(`${userData.username}:${userData.password}`)}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(urlToServer)
                })

                const data = await response.json()
                // this.msg = data.msg
                this.url = ''   
                if (data.short_url) {
                    this.short_url = data.short_url
                }        
            },

            
        }
    }
</script>