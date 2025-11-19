<template>
  <div id="app">
    <h1>Сервис добавления эмодзи по центру в видео</h1>
    <VideoProcessor />
  </div>
</template>

<script>
import VideoProcessor from './components/VideoProcessor.vue'

export default {
  name: 'App',
  components: {
    VideoProcessor
  }
}
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>