<template>
  <v-container fluid class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="custom-card">
          <v-card-title class="justify-center custom-title">
            Загрузка и скачивание видео
          </v-card-title>
          <v-card-text class="text-center">
            <!-- Скрытое поле выбора файла -->
            <input
              type="file"
              ref="fileInput"
              accept="video/*"
              @change="handleFileChange"
              style="display: none"
            />
            
            <!-- Кнопка загрузки -->
            <v-btn
              debugger
              v-if="!uploaded"
              color="primary"
              @click="triggerFileInput"
              :loading="loading"
              class="custom-button upload-btn"
            >
              Загрузить видео
            </v-btn>

            <!-- Кнопка скачивания -->
            <v-btn
              v-if="uploaded"
              color="success"
              @click="downloadVideo"
              class="custom-button download-btn"
            >
              Скачать {{ filename }}
            </v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      file: null,
      filename: '',
      uploaded: false,
      loading: false
    };
  },
  methods: {
    // Открывает диалоговое окно для выбора файла
    triggerFileInput() {
      this.$refs.fileInput.click();
    },
    // Обработчик события выбора файла
    handleFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.file = file;
        console.log("Файл выбран:", file.name); // Отладка: вывод имени файла в консоль
        this.uploadVideo();
      } else {
        console.warn("Файл не выбран");
      }
    },
    async uploadVideo() {
      console.log("Файл выбран:");
      if (!this.file) return;

      this.loading = true;
      const formData = new FormData();
      formData.append('file', this.file);

      try {
        const response = await axios.post('http://localhost:8000/video/upload/', formData, {
          headers: {
            'Content-Type': 'multipart/form-data'
          }
        });
        this.filename = response.data.filename;
        this.uploaded = true;
      } catch (error) {
        console.error('Ошибка при загрузке видео:', error);
      } finally {
        this.loading = false;
      }
    },
    async downloadVideo() {
      try {
        // Отправляем POST запрос для скачивания видео
        const response = await axios.post(
          'http://localhost:8000/video/download/', // Ваш API эндпоинт
          { "filename": this.filename }, // Отправляем имя файла
          {
            responseType: 'blob', // Ожидаем бинарные данные (файл)
          }
        );

        // Создаем URL для скачивания файла
        const url = window.URL.createObjectURL(new Blob([response.data]));
        
        // Создаем временную ссылку для скачивания
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', this.filename); // Имя файла, под которым он будет сохранен
        document.body.appendChild(link);
        
        // Имитируем клик по ссылке для начала скачивания
        link.click();
        
        // Удаляем ссылку из DOM после скачивания
        document.body.removeChild(link);

      } catch (error) {
        console.error("Ошибка при скачивании файла:", error);
      }
    }
  }
};
</script>

<style scoped>
/* Основной фон и выравнивание */
.fill-height {
  background-color: #f0f4f8; /* Легкий фоновый цвет */
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 20px;
}

/* Карточка с содержимым */
.custom-card {
  background-color: #ffffff; /* Белый фон для карточки */
  border-radius: 15px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  padding: 40px;
  display: flex;
  flex-direction: column;
  justify-content: space-between; /* Пространство между кнопками */
}

/* Заголовок */
.custom-title {
  font-size: 2rem;
  font-weight: bold;
  color: #3f51b5;
  margin-bottom: 20px;
}

/* Стиль для файла-выбора */
.custom-file-input {
  margin-bottom: 20px;
}

/* Кнопки */
.custom-button {
  font-size: 1.2rem;
  padding: 15px 30px;
  transition: background-color 0.3s ease;
  border-radius: 8px;
  width: 100%;
  margin-top: 15px;
}

/* Кнопка загрузки */
.upload-btn {
  background-color: #3f51b5;
  color: #fff;
}

.upload-btn:hover {
  background-color: #303f9f;
}

/* Кнопка скачивания */
.download-btn {
  background-color: #4caf50;
  color: #fff;
}

.download-btn:hover {
  background-color: #388e3c;
}
</style>
