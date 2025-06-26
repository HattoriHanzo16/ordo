<template>
  <div class="min-h-screen bg-secondary-50">
    <!-- Navigation Bar -->
    <NavBar />
    
    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Header Section -->
      <div class="mb-8">
        <h1 class="text-4xl font-bold text-dark-900 mb-4">Your Recordings</h1>
        <p class="text-lg text-dark-600 max-w-2xl">
          View, search, and manage all your meeting recordings and transcripts in one place.
        </p>
      </div>

      <!-- Search and Filter Bar -->
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
        <div class="flex flex-col md:flex-row gap-4 items-start md:items-center justify-between">
          <div class="flex-1 max-w-md">
            <div class="relative">
              <svg class="w-5 h-5 text-dark-400 absolute left-3 top-1/2 transform -translate-y-1/2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
              <input
                v-model="searchQuery"
                type="text"
                placeholder="Search recordings..."
                class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
                @input="performSearch"
              />
            </div>
          </div>
          
          <div class="flex gap-3">
            <select 
              v-model="statusFilter"
              @change="applyFilters"
              class="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-primary-500 transition-colors"
            >
              <option value="">All Status</option>
              <option value="completed">Completed</option>
              <option value="processing">Processing</option>
              <option value="pending">Pending</option>
              <option value="error">Error</option>
            </select>
            
            <button 
              @click="refreshRecordings"
              :disabled="loading"
              class="btn-secondary flex items-center"
            >
              <svg 
                class="w-4 h-4 mr-2" 
                :class="{ 'animate-spin': loading }"
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"></path>
              </svg>
              Refresh
            </button>
          </div>
        </div>
      </div>

      <!-- Statistics Cards -->
      <div class="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-primary-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2zm12-3c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-dark-500">Total Recordings</p>
              <p class="text-2xl font-bold text-dark-900">{{ totalRecordings }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-dark-500">Completed</p>
              <p class="text-2xl font-bold text-dark-900">{{ completedCount }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-dark-500">Processing</p>
              <p class="text-2xl font-bold text-dark-900">{{ processingCount }}</p>
            </div>
          </div>
        </div>
        
        <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-200">
          <div class="flex items-center">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center">
              <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
            </div>
            <div class="ml-4">
              <p class="text-sm text-dark-500">Total Duration</p>
              <p class="text-2xl font-bold text-dark-900">{{ totalDuration }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- Loading State -->
      <div v-if="loading && recordings.length === 0" class="flex justify-center items-center py-12">
        <div class="text-center">
          <svg class="animate-spin h-8 w-8 text-primary-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="text-dark-600">Loading recordings...</p>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else-if="!loading && filteredRecordings.length === 0" class="text-center py-12">
        <div class="w-24 h-24 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2zm12-3c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2z"></path>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-dark-900 mb-2">
          {{ searchQuery || statusFilter ? 'No recordings match your filters' : 'No recordings yet' }}
        </h3>
        <p class="text-dark-600 mb-6 max-w-md mx-auto">
          {{ searchQuery || statusFilter ? 'Try adjusting your search or filter criteria.' : 'Start by uploading your first meeting recording to see it here.' }}
        </p>
        <router-link to="/" class="btn-primary">
          Upload Your First Recording
        </router-link>
      </div>

      <!-- Recordings Grid -->
      <div v-else class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-8">
        <div 
          v-for="recording in paginatedRecordings" 
          :key="recording.id"
          class="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow duration-200"
        >
          <!-- Recording Card Header -->
          <div class="p-6 border-b border-gray-100">
            <div class="flex items-start justify-between mb-3">
              <div class="flex-1">
                <h3 class="font-semibold text-dark-900 mb-1 truncate" :title="recording.original_filename">
                  {{ recording.original_filename }}
                </h3>
                <div class="flex items-center space-x-2 mb-1">
                  <p class="text-sm text-dark-500">{{ formatDate(recording.created_at) }}</p>
                  <!-- Labels -->
                  <div v-if="recording.labels && recording.labels.length" class="flex items-center space-x-1">
                    <span
                      v-for="label in recording.labels"
                      :key="label.label_name"
                      class="inline-flex items-center justify-center px-2.5 py-1 rounded-full text-xs font-medium text-white whitespace-nowrap"
                      :style="{ backgroundColor: label.label_color }"
                      :title="`Confidence: ${Math.round((label.confidence || 0.8) * 100)}%`"
                    >
                      {{ label.label_name }}
                    </span>
                  </div>
                </div>
              </div>
              <div class="ml-3">
                <span 
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium"
                  :class="getStatusBadgeClass(recording.processing_status)"
                >
                  <span 
                    class="w-1.5 h-1.5 rounded-full mr-1.5"
                    :class="getStatusDotClass(recording.processing_status)"
                  ></span>
                  {{ formatStatus(recording.processing_status) }}
                </span>
              </div>
            </div>
            
            <!-- File Info -->
            <div class="flex items-center text-sm text-dark-500 space-x-4">
              <span class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                {{ formatFileSize(recording.file_size) }}
              </span>
              <span v-if="recording.duration" class="flex items-center">
                <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                {{ formatDuration(recording.duration) }}
              </span>
            </div>
          </div>

          <!-- Recording Card Body -->
          <div class="p-6">
            <!-- Transcript Preview -->
            <div v-if="recording.transcript" class="mb-4">
              <h4 class="text-sm font-medium text-dark-900 mb-2">Transcript Preview</h4>
              <p class="text-sm text-dark-600 line-clamp-3 bg-gray-50 p-3 rounded-lg">
                {{ recording.transcript.substring(0, 150) }}{{ recording.transcript.length > 150 ? '...' : '' }}
              </p>
            </div>

            <!-- Error Message -->
            <div v-else-if="recording.processing_error" class="mb-4">
              <div class="bg-red-50 border border-red-200 rounded-lg p-3">
                <p class="text-sm text-red-700">
                  <svg class="w-4 h-4 inline mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  {{ recording.processing_error }}
                </p>
              </div>
            </div>

            <!-- Processing State -->
            <div v-if="isProcessing(recording.processing_status)" class="mb-4">
              <div class="bg-blue-50 border border-blue-200 rounded-lg p-3">
                <p class="text-sm text-blue-700 flex items-center">
                  <svg class="animate-spin w-4 h-4 mr-2" fill="none" viewBox="0 0 24 24">
                    <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                    <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  {{ getProcessingMessage(recording.processing_status) }}
                </p>
                
                <!-- Processing Progress Bar -->
                <div class="mt-2 bg-blue-200 rounded-full h-1.5">
                  <div 
                    class="bg-blue-500 h-1.5 rounded-full transition-all duration-500"
                    :style="{ width: getProcessingProgress(recording.processing_status) + '%' }"
                  ></div>
                </div>
              </div>
            </div>
            
            <!-- Pending State -->
            <div v-else-if="recording.processing_status === 'pending'" class="mb-4">
              <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                <p class="text-sm text-yellow-700 flex items-center">
                  <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                  </svg>
                  Queued for processing...
                </p>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-2">
              <router-link 
                v-if="recording.processing_status === 'completed'"
                :to="`/recordings/${recording.id}`"
                class="flex-1 btn-primary text-sm py-2 text-center no-underline"
              >
                View Details
              </router-link>
              <button 
                v-if="recording.media_url"
                @click="playRecording(recording)"
                class="flex-1 btn-secondary text-sm py-2"
              >
                Play Audio
              </button>
              <button 
                v-if="recording.processing_status === 'completed' && recording.summary"
                @click="labelRecording(recording.id)"
                :disabled="labelingInProgress[recording.id]"
                class="flex items-center gap-2 px-3 py-2 text-purple-600 hover:text-purple-700 hover:bg-purple-50 border border-purple-200 hover:border-purple-300 rounded-lg transition-colors disabled:opacity-50 disabled:cursor-not-allowed text-sm font-medium"
              >
                <svg v-if="!labelingInProgress[recording.id]" class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
                </svg>
                <svg v-else class="w-4 h-4 animate-spin" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                </svg>
                <span v-if="!labelingInProgress[recording.id]">Label with AI</span>
                <span v-else>Labeling...</span>
              </button>
              <button 
                @click="deleteRecording(recording.id)"
                class="px-3 py-2 text-red-600 hover:text-red-700 hover:bg-red-50 rounded-lg transition-colors"
                :title="'Delete ' + recording.original_filename"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Load More Button -->
      <div v-if="hasMoreRecordings && !loading" class="text-center">
        <button 
          @click="loadMoreRecordings"
          class="btn-secondary"
        >
          Load More Recordings
        </button>
      </div>
    </main>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'

export default {
  name: 'RecordingsPage',
  components: {
    NavBar
  },
  data() {
    return {
      recordings: [],
      totalRecordings: 0,
      loading: false,
      searchQuery: '',
      statusFilter: '',
      currentPage: 0,
      pageSize: 12,
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
      pollingInterval: null,
      labelingInProgress: {}
    }
  },
  computed: {
    filteredRecordings() {
      let filtered = [...this.recordings]
      
      // Apply search filter
      if (this.searchQuery.trim()) {
        const query = this.searchQuery.toLowerCase()
        filtered = filtered.filter(recording => 
          recording.original_filename.toLowerCase().includes(query) ||
          (recording.transcript && recording.transcript.toLowerCase().includes(query))
        )
      }
      
      // Apply status filter
      if (this.statusFilter) {
        filtered = filtered.filter(recording => 
          recording.processing_status === this.statusFilter
        )
      }
      
      return filtered
    },
    
    paginatedRecordings() {
      const start = 0
      const end = (this.currentPage + 1) * this.pageSize
      return this.filteredRecordings.slice(start, end)
    },
    
    hasMoreRecordings() {
      return this.paginatedRecordings.length < this.filteredRecordings.length
    },
    
    completedCount() {
      return this.recordings.filter(r => r.processing_status === 'completed').length
    },
    
    processingCount() {
      return this.recordings.filter(r => 
        ['pending', 'processing', 'analyzing', 'generating_visuals'].includes(r.processing_status)
      ).length
    },
    
    totalDuration() {
      const total = this.recordings.reduce((sum, r) => sum + (r.duration || 0), 0)
      return this.formatDuration(total)
    }
  },
  methods: {
    async fetchRecordings() {
      this.loading = true
      try {
        const response = await fetch(`${this.apiBaseUrl}/api/v1/recordings?limit=1000`)
        if (!response.ok) throw new Error('Failed to fetch recordings')
        
        const data = await response.json()
        this.recordings = data.recordings || []
        this.totalRecordings = data.total || 0
      } catch (error) {
        console.error('Error fetching recordings:', error)
        // You might want to show a toast notification here
      } finally {
        this.loading = false
      }
    },
    
    async refreshRecordings() {
      await this.fetchRecordings()
    },
    
    // Removed auto-polling - users can manually refresh if needed
    
    async deleteRecording(recordingId) {
      if (!confirm('Are you sure you want to delete this recording? This action cannot be undone.')) {
        return
      }
      
      try {
        const response = await fetch(`${this.apiBaseUrl}/api/v1/recordings/${recordingId}`, {
          method: 'DELETE'
        })
        
        if (!response.ok) throw new Error('Failed to delete recording')
        
        // Remove from local state
        this.recordings = this.recordings.filter(r => r.id !== recordingId)
        this.totalRecordings -= 1
        
        // You might want to show a success toast here
      } catch (error) {
        console.error('Error deleting recording:', error)
        // You might want to show an error toast here
      }
    },
    

    
    async labelRecording(recordingId) {
      console.log('Starting labeling for recording:', recordingId)
      try {
        // Set loading state
        this.labelingInProgress[recordingId] = true
        
        const response = await fetch(`${this.apiBaseUrl}/api/v1/labeling/apply/${recordingId}`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          }
        })
        
        console.log('Response status:', response.status)
        
        if (!response.ok) {
          const error = await response.json()
          throw new Error(error.detail || 'Failed to apply labels')
        }
        
        const appliedLabels = await response.json()
        console.log('Applied labels:', appliedLabels)
        
        // Update the recording with new labels
        const recordingIndex = this.recordings.findIndex(r => r.id === recordingId)
        if (recordingIndex !== -1) {
          this.recordings[recordingIndex].labels = appliedLabels
        }
        
        // Show success message
        if (appliedLabels.length > 0) {
          console.log(`Applied ${appliedLabels.length} labels to recording`)
          // You might want to show a toast notification here
        } else {
          console.log('No labels were applied to this recording')
          // You might want to show an info message here
        }
        
      } catch (error) {
        console.error('Error applying labels:', error)
        // You might want to show an error toast here
      } finally {
        this.labelingInProgress[recordingId] = false
      }
    },

    playRecording(recording) {
      // Open the audio file in a new tab or implement an audio player
      window.open(recording.media_url, '_blank')
    },
    
    loadMoreRecordings() {
      this.currentPage += 1
    },
    
    performSearch() {
      // Reset pagination when searching
      this.currentPage = 0
    },
    
    applyFilters() {
      // Reset pagination when filtering
      this.currentPage = 0
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    },
    
    formatFileSize(bytes) {
      if (!bytes) return 'Unknown size'
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(1024))
      return Math.round(bytes / Math.pow(1024, i) * 100) / 100 + ' ' + sizes[i]
    },
    
    formatDuration(seconds) {
      if (!seconds) return '0:00'
      const hours = Math.floor(seconds / 3600)
      const minutes = Math.floor((seconds % 3600) / 60)
      const secs = Math.floor(seconds % 60)
      
      if (hours > 0) {
        return `${hours}:${minutes.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`
      }
      return `${minutes}:${secs.toString().padStart(2, '0')}`
    },
    
    formatStatus(status) {
      const statusMap = {
        'completed': 'Completed',
        'processing': 'Transcribing',
        'analyzing': 'Analyzing',
        'generating_visuals': 'Generating AI Visuals',
        'pending': 'Pending',
        'failed': 'Failed',
        'error': 'Error'
      }
      return statusMap[status] || status
    },
    
    isProcessing(status) {
      return ['processing', 'analyzing', 'generating_visuals'].includes(status)
    },
    
    getProcessingMessage(status) {
      const messages = {
        'processing': 'Transcribing audio...',
        'analyzing': 'Analyzing content & extracting insights...',
        'generating_visuals': 'Creating AI-powered visual summary...'
      }
      return messages[status] || 'Processing...'
    },
    
    getProcessingProgress(status) {
      const progress = {
        'pending': 0,
        'processing': 40,
        'analyzing': 70,
        'generating_visuals': 90,
        'completed': 100
      }
      return progress[status] || 0
    },
    
    getStatusBadgeClass(status) {
      const classes = {
        'completed': 'bg-green-100 text-green-800',
        'processing': 'bg-blue-100 text-blue-800',
        'analyzing': 'bg-purple-100 text-purple-800',
        'generating_visuals': 'bg-pink-100 text-pink-800',
        'pending': 'bg-yellow-100 text-yellow-800',
        'failed': 'bg-red-100 text-red-800',
        'error': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },
    
    getStatusDotClass(status) {
      const classes = {
        'completed': 'bg-green-400',
        'processing': 'bg-blue-400',
        'analyzing': 'bg-purple-400',
        'generating_visuals': 'bg-pink-400',
        'pending': 'bg-yellow-400',
        'failed': 'bg-red-400',
        'error': 'bg-red-400'
      }
      return classes[status] || 'bg-gray-400'
    }
  },
  
  mounted() {
    this.fetchRecordings()
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

.no-underline {
  text-decoration: none;
}

.no-underline:hover {
  text-decoration: none;
}
</style> 