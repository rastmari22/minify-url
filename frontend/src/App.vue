<!-- <template>
  <div id="app">
    <img src="./assets/logo.png">
    <router-view/>
  </div>
</template>

<script>
export default {
  name: 'App'
}
</script>

<style>
#app {
  margin-top: 60px
}
</style> -->

<template>
  <div>
    <router-view></router-view>
  </div>
</template>

<script>

  export default {
    data() {
      return {
        info: "Title",
        someInfo: "Anons of message",
      }
    },
    methods: {
      userData() {
        this.info = 'Some new info'
      },

    }
  }
</script>

<style>
  h3 {
    font-weight: lighter;
  }
  p {
    color: rebeccapurple;
  }
  #app {
  margin-top: 60px
}
</style>