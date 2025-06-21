<template>
  <div class="min-h-screen bg-secondary-50">
    <!-- Navigation Bar -->
    <NavBar />
    
    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Hero Section -->
      <div class="text-center mb-12 animate-fade-in">
        <h1 class="text-4xl font-bold text-dark-900 mb-4">
          Welcome to <span class="text-primary-500">Ordo</span>
        </h1>
        <p class="text-lg text-dark-600 max-w-2xl mx-auto">
          Your intelligent recording management system. Upload, organize, and manage your media files with ease.
        </p>
      </div>
      
      <!-- Upload Section -->
      <UploadSection />
      
      <!-- Recent Recordings Section -->
      <section class="mt-16 animate-slide-up">
        <h2 class="text-2xl font-semibold text-dark-900 mb-6">Recent Recordings</h2>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div v-for="i in 6" :key="i" class="card opacity-50">
            <div class="flex items-center space-x-4">
              <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
                <svg class="w-6 h-6 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2zm12-3c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2z"></path>
                </svg>
              </div>
              <div class="flex-1">
                <h3 class="font-medium text-dark-900">Sample Recording {{ i }}</h3>
                <p class="text-sm text-dark-500">No recordings yet</p>
              </div>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import NavBar from './components/NavBar.vue'
import UploadSection from './components/UploadSection.vue'

export default {
  name: 'App',
  components: {
    NavBar,
    UploadSection
  }
}
</script> 