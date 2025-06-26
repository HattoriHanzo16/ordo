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
          <router-link 
            v-for="item in navItems" 
            :key="item.name"
            :to="item.path"
            class="text-dark-600 hover:text-primary-500 font-medium transition-colors duration-200"
            :class="{ 'text-primary-500': $route.path === item.path }"
          >
            {{ item.name }}
          </router-link>
        </div>
        
        <!-- Search Bar -->
        <div class="hidden md:flex items-center flex-1 max-w-lg mx-8">
          <div class="relative w-full">
            <input
              v-model="searchQuery"
              @input="handleSearchInput"
              @keyup.enter="performSearch"
              type="text"
              placeholder="Search recordings, transcripts, and summaries..."
              class="w-full px-4 py-2 pr-10 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
            />
            <button
              @click="performSearch"
              class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-primary-500"
            >
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </button>
          </div>
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
          <router-link 
            v-for="item in navItems" 
            :key="item.name"
            :to="item.path"
            class="text-dark-600 hover:text-primary-500 font-medium transition-colors duration-200 py-2"
            :class="{ 'text-primary-500': $route.path === item.path }"
          >
            {{ item.name }}
          </router-link>
          <div class="pt-4 border-t border-gray-200">
            <div class="relative">
              <input
                v-model="searchQuery"
                @input="handleSearchInput"
                @keyup.enter="performSearch"
                type="text"
                placeholder="Search recordings, transcripts, and summaries..."
                class="w-full px-4 py-2 pr-10 text-sm border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 outline-none"
              />
              <button
                @click="performSearch"
                class="absolute right-2 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-primary-500"
              >
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>
      
      <!-- Search Results Dropdown -->
      <div v-if="showSearchResults && searchResults.length > 0" class="absolute top-full left-0 right-0 bg-white shadow-lg border border-gray-200 rounded-lg mt-1 max-h-96 overflow-y-auto z-50">
        <div class="p-2">
          <div class="text-sm text-gray-500 px-3 py-2 border-b">
            Found {{ searchResults.length }} results
          </div>
          <div
            v-for="result in searchResults"
            :key="`${result.recording_id}-${result.chunk_id}`"
            @click="navigateToRecording(result.recording_id)"
            class="p-3 hover:bg-gray-50 cursor-pointer border-b border-gray-100 last:border-b-0"
          >
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <div class="font-medium text-sm text-gray-900 mb-1">
                  {{ result.recording_title }}
                </div>
                <div class="text-xs text-gray-600 mb-2">
                  {{ formatDate(result.created_at) }}
                  <span v-if="result.duration" class="mx-1">•</span>
                  <span v-if="result.duration">{{ formatDuration(result.duration) }}</span>
                </div>
                <div class="text-sm text-gray-700 line-clamp-3">
                  {{ truncateText(result.chunk_text, 150) }}
                </div>
              </div>
              <div class="ml-3 text-xs text-primary-600 font-medium">
                {{ Math.round(result.similarity * 100) }}% match
              </div>
            </div>
          </div>
        </div>
      </div>
      
      <!-- No Results -->
      <div v-else-if="showSearchResults && searchResults.length === 0 && !searchLoading && searchQuery.trim()" class="absolute top-full left-0 right-0 bg-white shadow-lg border border-gray-200 rounded-lg mt-1 z-50">
        <div class="p-4 text-center text-gray-500">
          <svg class="w-8 h-8 mx-auto mb-2 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6-4h6m2 5.291A7.962 7.962 0 0112 15c-4.411 0-8-3.589-8-8s3.589-8 8-8 8 3.589 8 8a7.962 7.962 0 01-2.291 5.291z"></path>
          </svg>
          <div class="text-sm">No results found for "{{ searchQuery }}"</div>
          <div class="text-xs text-gray-400 mt-1">Try different keywords or check if recordings have been transcribed and analyzed</div>
        </div>
      </div>
      
      <!-- Loading -->
      <div v-else-if="searchLoading" class="absolute top-full left-0 right-0 bg-white shadow-lg border border-gray-200 rounded-lg mt-1 z-50">
        <div class="p-4 text-center">
          <div class="inline-flex items-center text-sm text-gray-600">
            <svg class="animate-spin -ml-1 mr-2 h-4 w-4 text-primary-500" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            Searching...
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
      searchQuery: '',
      searchResults: [],
      showSearchResults: false,
      searchLoading: false,
      searchTimeout: null,
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
      navItems: [
        { name: 'Home', path: '/' },
        { name: 'Recordings', path: '/recordings' },
        { name: 'Settings', path: '/settings' }
      ]
    }
  },
  mounted() {
    // Close search results when clicking outside
    document.addEventListener('click', this.handleClickOutside)
  },
  beforeUnmount() {
    document.removeEventListener('click', this.handleClickOutside)
  },
  methods: {
    toggleMobileMenu() {
      this.mobileMenuOpen = !this.mobileMenuOpen
    },
    
    handleSearchInput() {
      // Clear previous timeout
      if (this.searchTimeout) {
        clearTimeout(this.searchTimeout)
      }
      
      // If search query is empty, hide results
      if (!this.searchQuery.trim()) {
        this.showSearchResults = false
        this.searchResults = []
        return
      }
      
      // Debounce search - wait 300ms after user stops typing
      this.searchTimeout = setTimeout(() => {
        this.performSearch()
      }, 300)
    },
    
    async performSearch() {
      if (!this.searchQuery.trim()) {
        this.showSearchResults = false
        return
      }
      
      this.searchLoading = true
      this.showSearchResults = true
      
      try {
        const response = await fetch(`${this.apiBaseUrl}/api/v1/search/semantic?query=${encodeURIComponent(this.searchQuery)}&limit=10`)
        
        if (!response.ok) {
          throw new Error('Search failed')
        }
        
        const data = await response.json()
        this.searchResults = data.results || []
        
      } catch (error) {
        console.error('Search error:', error)
        this.searchResults = []
      } finally {
        this.searchLoading = false
      }
    },
    
    navigateToRecording(recordingId) {
      this.showSearchResults = false
      this.searchQuery = ''
      this.$router.push(`/recordings/${recordingId}`)
    },
    
    handleClickOutside(event) {
      // Check if click is outside the search area
      const searchContainer = event.target.closest('.relative')
      if (!searchContainer || !searchContainer.querySelector('input[type="text"]')) {
        this.showSearchResults = false
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        month: 'short',
        day: 'numeric',
        year: 'numeric'
      })
    },
    
    formatDuration(seconds) {
      if (!seconds) return ''
      
      const minutes = Math.floor(seconds / 60)
      const remainingSeconds = Math.floor(seconds % 60)
      
      if (minutes > 60) {
        const hours = Math.floor(minutes / 60)
        const remainingMinutes = minutes % 60
        return `${hours}h ${remainingMinutes}m`
      }
      
      return `${minutes}m ${remainingSeconds}s`
    },
    
    truncateText(text, maxLength) {
      if (!text) return ''
      if (text.length <= maxLength) return text
      return text.substring(0, maxLength) + '...'
    }
  }
}
</script>

<style scoped>
.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style> 