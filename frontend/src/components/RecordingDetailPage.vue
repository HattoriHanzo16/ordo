<template>
  <div class="min-h-screen bg-secondary-50">
    <!-- Navigation Bar -->
    <NavBar />
    
    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="text-center">
          <svg class="animate-spin h-8 w-8 text-primary-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          <p class="text-dark-600">Loading recording details...</p>
        </div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <div class="w-24 h-24 bg-red-100 rounded-full flex items-center justify-center mx-auto mb-6">
          <svg class="w-12 h-12 text-red-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
          </svg>
        </div>
        <h3 class="text-xl font-semibold text-dark-900 mb-2">Recording Not Found</h3>
        <p class="text-dark-600 mb-6">{{ error }}</p>
        <router-link to="/recordings" class="btn-primary">
          Back to Recordings
        </router-link>
      </div>

      <!-- Recording Details -->
      <div v-else-if="recording" class="space-y-8">
        <!-- Header Section -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
          <div class="flex items-start justify-between mb-4">
            <div class="flex-1">
              <div class="flex items-center mb-2">
                <router-link to="/recordings" class="text-dark-500 hover:text-dark-700 mr-3">
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7"></path>
                  </svg>
                </router-link>
                <h1 class="text-3xl font-bold text-dark-900">{{ recording.original_filename }}</h1>
              </div>
              <p class="text-dark-600 mb-4">{{ formatDate(recording.created_at) }}</p>
              
              <!-- Status Badge -->
              <span 
                class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium"
                :class="getStatusBadgeClass(recording.processing_status)"
              >
                <span 
                  class="w-2 h-2 rounded-full mr-2"
                  :class="getStatusDotClass(recording.processing_status)"
                ></span>
                {{ formatStatus(recording.processing_status) }}
              </span>
            </div>
            
            <!-- Action Buttons -->
            <div class="flex gap-3">
              <button 
                v-if="recording.media_url"
                @click="playRecording"
                class="btn-secondary flex items-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M14.828 14.828a4 4 0 01-5.656 0M9 10h1.586a1 1 0 01.707.293l2.414 2.414a1 1 0 00.707.293H15M9 10v4a2 2 0 002 2h2a2 2 0 002-2v-4M9 10V9a2 2 0 012-2h2a2 2 0 012 2v1"></path>
                </svg>
                Play Audio
              </button>
              <button 
                @click="deleteRecording"
                class="btn-secondary text-red-600 hover:text-red-700 hover:bg-red-50 flex items-center"
              >
                <svg class="w-4 h-4 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                </svg>
                Delete
              </button>
            </div>
          </div>
          
          <!-- File Info -->
          <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mt-6">
            <div class="flex items-center text-sm text-dark-600">
              <svg class="w-5 h-5 text-dark-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
              <span>{{ formatFileSize(recording.file_size) }}</span>
            </div>
            <div v-if="recording.duration" class="flex items-center text-sm text-dark-600">
              <svg class="w-5 h-5 text-dark-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>{{ formatDuration(recording.duration) }}</span>
            </div>
            <div v-if="recording.content_type" class="flex items-center text-sm text-dark-600">
              <svg class="w-5 h-5 text-dark-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 4V2a1 1 0 011-1h4a1 1 0 011 1v2h4a1 1 0 011 1v2a1 1 0 01-1 1h-1v9a2 2 0 01-2 2H8a2 2 0 01-2-2V8H5a1 1 0 01-1-1V5a1 1 0 011-1h2z"></path>
              </svg>
              <span>{{ recording.content_type }}</span>
            </div>
            <div class="flex items-center text-sm text-dark-600">
              <svg class="w-5 h-5 text-dark-400 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"></path>
              </svg>
              <span>Updated {{ formatDate(recording.updated_at) }}</span>
            </div>
          </div>
        </div>

        <!-- Error Message -->
        <div v-if="recording.processing_error" class="bg-red-50 border border-red-200 rounded-xl p-6">
          <div class="flex items-start">
            <svg class="w-6 h-6 text-red-500 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <div>
              <h3 class="text-lg font-semibold text-red-800 mb-2">Processing Error</h3>
              <p class="text-red-700">{{ recording.processing_error }}</p>
            </div>
          </div>
        </div>

        <!-- Content Grid -->
        <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
          <!-- Left Column - Summary and Analysis -->
          <div class="xl:col-span-2 space-y-6">
            
            <!-- Decision Tree -->
            <div v-if="recording.visual_summary_url" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 class="text-xl font-semibold text-dark-900 mb-4 flex items-center">
                <svg class="w-6 h-6 text-purple-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"></path>
                </svg>
                Decision Tree
                <span class="ml-2 text-xs bg-purple-100 text-purple-800 px-2 py-1 rounded-full">AI Generated</span>
              </h2>
              <div class="relative">
                <img 
                  :src="recording.visual_summary_url" 
                  :alt="`Decision tree for ${recording.original_filename}`"
                  class="w-full max-w-lg mx-auto rounded-lg shadow-md hover:shadow-lg transition-shadow cursor-pointer"
                  @click="openImageModal"
                  @error="handleImageError"
                />
                <div class="mt-3 text-center">
                  <p class="text-sm text-dark-600">AI-generated decision flowchart based on action items and decisions</p>
                  <button 
                    @click="openImageModal"
                    class="mt-2 text-sm text-primary-600 hover:text-primary-800 font-medium"
                  >
                    View Full Size
                  </button>
                </div>
              </div>
            </div>
            <!-- Summary -->
            <div v-if="recording.summary" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 class="text-xl font-semibold text-dark-900 mb-4 flex items-center">
                <svg class="w-6 h-6 text-primary-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Summary
              </h2>
              <div class="prose prose-sm max-w-none text-dark-700">
                <p>{{ recording.summary }}</p>
              </div>
            </div>

            <!-- Action Items -->
            <div v-if="recording.action_items" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 class="text-xl font-semibold text-dark-900 mb-4 flex items-center">
                <svg class="w-6 h-6 text-orange-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-6 9l2 2 4-4"></path>
                </svg>
                Action Items
                <span class="ml-2 text-sm bg-orange-100 text-orange-800 px-2 py-1 rounded-full">{{ recording.action_items?.length || 0 }}</span>
              </h2>
              <div v-if="recording.action_items && recording.action_items.length > 0" class="space-y-3">
                <div v-for="(item, index) in recording.action_items" :key="index" class="flex items-start space-x-3 p-3 bg-orange-50 rounded-lg border border-orange-100">
                  <div class="w-2 h-2 bg-orange-400 rounded-full mt-2"></div>
                  <div class="flex-1">
                    <p class="text-dark-800">{{ item.description }}</p>
                    <div v-if="item.assignee || item.due_date || item.priority" class="flex flex-wrap gap-2 mt-2">
                      <span v-if="item.assignee" class="text-xs bg-gray-100 text-gray-700 px-2 py-1 rounded">
                        Assignee: {{ item.assignee }}
                      </span>
                      <span v-if="item.due_date" class="text-xs bg-blue-100 text-blue-700 px-2 py-1 rounded">
                        Due: {{ item.due_date }}
                      </span>
                      <span v-if="item.priority" class="text-xs px-2 py-1 rounded" :class="getPriorityClass(item.priority)">
                        {{ item.priority }} Priority
                      </span>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            <!-- Decisions -->
            <div v-if="recording.decisions" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 class="text-xl font-semibold text-dark-900 mb-4 flex items-center">
                <svg class="w-6 h-6 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Decisions Made
                <span class="ml-2 text-sm bg-green-100 text-green-800 px-2 py-1 rounded-full">{{ recording.decisions.length }}</span>
              </h2>
              <div class="space-y-3">
                <div v-for="(decision, index) in recording.decisions" :key="index" class="p-4 bg-green-50 rounded-lg border border-green-100">
                  <p class="text-dark-800 font-medium mb-2">{{ decision.description }}</p>
                  <div v-if="decision.owner || decision.context || decision.impact" class="space-y-1">
                    <p v-if="decision.owner" class="text-sm text-dark-600">
                      <span class="font-medium">Owner:</span> {{ decision.owner }}
                    </p>
                    <p v-if="decision.context" class="text-sm text-dark-600">
                      <span class="font-medium">Context:</span> {{ decision.context }}
                    </p>
                    <p v-if="decision.impact" class="text-sm text-dark-600">
                      <span class="font-medium">Impact:</span> {{ decision.impact }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

            <!-- Full Transcript -->
            <div v-if="recording.transcript" class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 class="text-xl font-semibold text-dark-900 mb-4 flex items-center">
                <svg class="w-6 h-6 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Full Transcript
              </h2>
              <div class="prose prose-sm max-w-none">
                <div class="bg-gray-50 rounded-lg p-4 max-h-96 overflow-y-auto">
                  <pre class="whitespace-pre-wrap text-dark-700 text-sm">{{ recording.transcript }}</pre>
                </div>
              </div>
            </div>
          </div>

          <!-- Right Column - Transcript with Speakers -->
          <div v-if="hasSpeakerDiarization" class="space-y-6">
            <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6">
              <h2 class="text-xl font-semibold text-dark-900 mb-4 flex items-center">
                <svg class="w-6 h-6 text-purple-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
                </svg>
                Speaker-Segmented Transcript
                <span v-if="!speakerDiarizationAvailable" class="ml-2 text-sm bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full">
                  Single Speaker
                </span>
              </h2>
              <div class="max-h-96 overflow-y-auto">
                <div class="space-y-3">
                  <pre class="whitespace-pre-wrap text-dark-700 text-sm">{{ recording.transcript_with_speakers }}</pre>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Speaker Diarization Not Available Notice -->
          <div v-else-if="recording.transcript && !recording.transcript_with_speakers" class="space-y-6">
            <div class="bg-yellow-50 border border-yellow-200 rounded-xl p-6">
              <div class="flex items-start">
                <svg class="w-6 h-6 text-yellow-500 mr-3 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z"></path>
                </svg>
                <div>
                  <h3 class="text-lg font-semibold text-yellow-800 mb-2">Speaker Identification Not Available</h3>
                  <p class="text-yellow-700 mb-3">Speaker diarization requires additional configuration. This may be because:</p>
                  <ul class="text-yellow-700 text-sm space-y-1 ml-4">
                    <li>• HuggingFace access token is not configured</li>
                    <li>• Only one speaker was detected in the recording</li>
                    <li>• The audio quality doesn't support speaker separation</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
    
    <!-- Image Modal -->
    <div v-if="showImageModal && recording?.visual_summary_url" class="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center z-50" @click="closeImageModal">
      <div class="relative max-w-4xl max-h-screen p-4">
        <button 
          @click="closeImageModal"
          class="absolute top-2 right-2 text-white hover:text-gray-300 z-10"
        >
          <svg class="w-8 h-8" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
          </svg>
        </button>
        <img 
          :src="recording.visual_summary_url" 
          :alt="`Decision tree for ${recording.original_filename}`"
          class="max-w-full max-h-full object-contain rounded-lg"
          @click.stop
        />
        <div class="absolute bottom-4 left-4 right-4 text-center">
          <p class="text-white text-sm bg-black bg-opacity-50 rounded px-3 py-2 inline-block">
            AI-generated decision tree for {{ recording.original_filename }}
          </p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'

export default {
  name: 'RecordingDetailPage',
  components: {
    NavBar
  },
  data() {
    return {
      recording: null,
      loading: false,
      error: null,
      showImageModal: false,
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    }
  },
  computed: {
    hasSpeakerDiarization() {
      if (!this.recording || !this.recording.transcript_with_speakers) {
        return false
      }
      
      // Check if the speaker transcript is different from regular transcript
      const normalTranscript = this.recording.transcript?.trim() || ''
      const speakerTranscript = this.recording.transcript_with_speakers?.trim() || ''
      
      // If they're the same, no real speaker diarization happened
      return normalTranscript !== speakerTranscript && speakerTranscript.length > 0
    },
    
    speakerDiarizationAvailable() {
      if (!this.recording || !this.recording.transcript_with_speakers) {
        return false
      }
      
      // Check if it contains multiple speakers or just formatted as single speaker
      const speakerTranscript = this.recording.transcript_with_speakers || ''
      const speakerMatches = speakerTranscript.match(/\[Speaker \w+\]:/g) || []
      const uniqueSpeakers = new Set(speakerMatches)
      
      return uniqueSpeakers.size > 1
    }
  },
  methods: {
    async fetchRecording() {
      this.loading = true
      this.error = null
      
      try {
        const response = await fetch(`${this.apiBaseUrl}/api/v1/recordings/${this.$route.params.id}`)
        
        if (!response.ok) {
          if (response.status === 404) {
            throw new Error('Recording not found')
          }
          throw new Error('Failed to fetch recording')
        }
        
        this.recording = await response.json()
      } catch (error) {
        console.error('Error fetching recording:', error)
        this.error = error.message
      } finally {
        this.loading = false
      }
    },
    
    async deleteRecording() {
      if (!confirm('Are you sure you want to delete this recording? This action cannot be undone.')) {
        return
      }
      
      try {
        const response = await fetch(`${this.apiBaseUrl}/api/v1/recordings/${this.recording.id}`, {
          method: 'DELETE'
        })
        
        if (!response.ok) throw new Error('Failed to delete recording')
        
        // Navigate back to recordings page
        this.$router.push('/recordings')
      } catch (error) {
        console.error('Error deleting recording:', error)
        alert('Failed to delete recording. Please try again.')
      }
    },
    
    playRecording() {
      if (this.recording.media_url) {
        window.open(this.recording.media_url, '_blank')
      }
    },
    
    formatDate(dateString) {
      const date = new Date(dateString)
      return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
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
        'processing': 'Processing',
        'pending': 'Pending',
        'error': 'Error'
      }
      return statusMap[status] || status
    },
    
    getStatusBadgeClass(status) {
      const classes = {
        'completed': 'bg-green-100 text-green-800',
        'processing': 'bg-blue-100 text-blue-800',
        'pending': 'bg-yellow-100 text-yellow-800',
        'error': 'bg-red-100 text-red-800'
      }
      return classes[status] || 'bg-gray-100 text-gray-800'
    },
    
    getStatusDotClass(status) {
      const classes = {
        'completed': 'bg-green-400',
        'processing': 'bg-blue-400',
        'pending': 'bg-yellow-400',
        'error': 'bg-red-400'
      }
      return classes[status] || 'bg-gray-400'
    },
    
    getPriorityClass(priority) {
      const classes = {
        'high': 'bg-red-100 text-red-800',
        'medium': 'bg-yellow-100 text-yellow-800',
        'low': 'bg-green-100 text-green-800'
      }
      return classes[priority?.toLowerCase()] || 'bg-gray-100 text-gray-800'
    },
    
    openImageModal() {
      this.showImageModal = true
    },
    
    closeImageModal() {
      this.showImageModal = false
    },
    
    handleImageError(event) {
      console.error('Failed to load visual summary image:', event)
      // Hide the visual summary section if image fails to load
      if (this.recording) {
        this.recording.visual_summary_url = null
      }
    }
  },
  
  mounted() {
    this.fetchRecording()
  },
  
  watch: {
    '$route.params.id'() {
      this.fetchRecording()
    }
  }
}
</script>

<style scoped>
.prose {
  line-height: 1.6;
}
</style> 