<template>
  <v-app>
    <v-main>
      <VideoPage />
    </v-main>
  </v-app>
</template>

<script>
import VideoPage from './components/VideoPage.vue';

export default {
  name: 'App',
  components: {
    VideoPage
  }
};
</script>

<style>
/* Добавьте стили по желанию */
</style>