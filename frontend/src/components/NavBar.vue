<template>
  <nav class="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-50">
    <div class="container mx-auto px-4">
      <div class="flex justify-between items-center h-16">
        <!-- Logo Section -->
        <div class="flex items-center space-x-3">
          <img 
            src="/logo.svg" 
            alt="Ordo Logo" 
            class="h-8 w-8"
          />
          <span class="text-xl font-bold text-dark-900">Ordo</span>
        </div>
        
        <!-- Desktop Navigation -->
        <div class="hidden md:flex items-center space-x-8">
          <a 
            v-for="item in navItems" 
            :key="item.name"
            :href="item.href"
            class="text-dark-600 hover:text-primary-500 font-medium transition-colors duration-200"
            :class="{ 'text-primary-500': item.active }"
          >
            {{ item.name }}
          </a>
        </div>
        
        <!-- Action Buttons -->
        <div class="hidden md:flex items-center space-x-4">
          <button class="btn-secondary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
            </svg>
            Search
          </button>
          <button class="btn-primary">
            <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
            </svg>
            New Recording
          </button>
        </div>
        
        <!-- Mobile Menu Button -->
        <div class="md:hidden">
          <button 
            @click="toggleMobileMenu"
            class="text-dark-600 hover:text-primary-500 focus:outline-none focus:text-primary-500 transition-colors duration-200"
          >
            <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path 
                v-if="!mobileMenuOpen"
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M4 6h16M4 12h16M4 18h16"
              ></path>
              <path 
                v-else
                stroke-linecap="round" 
                stroke-linejoin="round" 
                stroke-width="2" 
                d="M6 18L18 6M6 6l12 12"
              ></path>
            </svg>
          </button>
        </div>
      </div>
      
      <!-- Mobile Navigation -->
      <div v-if="mobileMenuOpen" class="md:hidden py-4 border-t border-gray-200">
        <div class="flex flex-col space-y-4">
          <a 
            v-for="item in navItems" 
            :key="item.name"
            :href="item.href"
            class="text-dark-600 hover:text-primary-500 font-medium transition-colors duration-200 py-2"
            :class="{ 'text-primary-500': item.active }"
          >
            {{ item.name }}
          </a>
          <div class="flex flex-col space-y-3 pt-4 border-t border-gray-200">
            <button class="btn-secondary justify-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              Search
            </button>
            <button class="btn-primary justify-center">
              <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"></path>
              </svg>
              New Recording
            </button>
          </div>
        </div>
      </div>
    </div>
  </nav>
</template>

<script>
export default {
  name: 'NavBar',
  data() {
    return {
      mobileMenuOpen: false,
      navItems: [
        { name: 'Dashboard', href: '#', active: true },
        { name: 'Recordings', href: '#', active: false },
        { name: 'Analytics', href: '#', active: false },
        { name: 'Settings', href: '#', active: false }
      ]
    }
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    }
  }
}
</script> 