<template>
  <div class="video-processor">
    <input type="file" @change="handleFileUpload" accept="video/mp4" />
    <button @click="processVideo" :disabled="!file || processing">
      {{ processing ? 'Обработка...' : 'Добавить 😊' }}
    </button>

    <div v-if="error" class="error">{{ error }}</div>

    <div v-if="processedVideoUrl" class="result">
      <h3>Результат:</h3>
      <video :src="processedVideoUrl" controls class="video-preview"></video>
      <br />
      <a :href="processedVideoUrl" :download="'emoji_video.mp4'">Скачать видео</a>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'VideoProcessor',
  data() {
    return {
      file: null,
      processing: false,
      processedVideoUrl: null,
      error: null
    }
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0]
      this.processedVideoUrl = null
      this.error = null
    },
    async processVideo() {
      if (!this.file) return

      this.processing = true
      this.error = null

      const formData = new FormData()
      formData.append('file', this.file)

      try {
        const response = await axios.post('/api/add-emoji', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          },
          responseType: 'blob'
        })

        const blob = new Blob([response.data], { type: 'video/mp4' })
        this.processedVideoUrl = URL.createObjectURL(blob)
      } catch (error) {
        this.error = error.response?.data?.detail || 'Произошла ошибка при обработке видео'
        console.error('Error processing video:', error)
      } finally {
        this.processing = false
      }
    }
  }
}
</script>

<style scoped>
.video-processor {
  max-width: 600px;
  margin: 0 auto;
}

input, button {
  margin: 10px;
  padding: 10px;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.video-preview {
  max-width: 100%;
  max-height: 400px;
  margin-top: 20px;
}

.error {
  color: red;
  margin-top: 10px;
}

.result {
  margin-top: 20px;
}
</style>