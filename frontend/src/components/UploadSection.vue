<template>
  <section class="mb-12 animate-slide-up">
    <div class="max-w-4xl mx-auto">
      <div class="text-center mb-8">
        <h2 class="text-3xl font-bold text-dark-900 mb-4">Upload Your Meeting Recording</h2>
        <p class="text-dark-600 mb-6">
          Drop your meeting files here for instant AI transcription and analysis
        </p>
        
        <!-- Supported Formats -->
        <div class="flex flex-wrap justify-center items-center gap-4 text-sm text-dark-500">
          <span class="bg-blue-100 text-blue-700 px-3 py-1 rounded-full font-medium flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2zm12-3c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2z"></path>
            </svg>
            MP3
          </span>
          <span class="bg-purple-100 text-purple-700 px-3 py-1 rounded-full font-medium flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
            </svg>
            MP4
          </span>
          <span class="bg-green-100 text-green-700 px-3 py-1 rounded-full font-medium flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2zm12-3c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2z"></path>
            </svg>
            WAV
          </span>
          <span class="bg-orange-100 text-orange-700 px-3 py-1 rounded-full font-medium flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2zm12-3c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2z"></path>
            </svg>
            M4A
          </span>
          <span class="bg-indigo-100 text-indigo-700 px-3 py-1 rounded-full font-medium flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
            </svg>
            MOV
          </span>
          <span class="bg-red-100 text-red-700 px-3 py-1 rounded-full font-medium flex items-center">
            <svg class="w-4 h-4 mr-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 10l4.553-2.276A1 1 0 0121 8.618v6.764a1 1 0 01-1.447.894L15 14M5 18h8a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
            </svg>
            AVI
          </span>
        </div>
      </div>
      
      <!-- Upload Area -->
      <div 
        class="relative border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-primary-400 transition-colors duration-300"
        :class="{
          'border-primary-500 bg-primary-50': isDragging,
          'border-red-400 bg-red-50': hasError,
          'border-green-400 bg-green-50': hasSuccess
        }"
        @drop.prevent="handleDrop"
        @dragover.prevent="handleDragOver"
        @dragenter.prevent="handleDragEnter"
        @dragleave.prevent="handleDragLeave"
      >
        <!-- Upload Icon and Text -->
        <div v-if="!uploadingFiles.length && !uploadedFiles.length" class="space-y-4">
          <div class="mx-auto w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center">
            <svg class="w-8 h-8 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
            </svg>
          </div>
          <div>
            <h3 class="text-lg font-semibold text-dark-900 mb-2">
              {{ isDragging ? 'Drop your meeting files here' : 'Upload your meeting recordings' }}
            </h3>
            <p class="text-dark-500 mb-4">
              Drop your meeting files here, or 
              <button 
                @click="triggerFileInput"
                class="text-primary-500 hover:text-primary-600 font-medium"
              >
                browse to choose files
              </button>
            </p>
            <p class="text-sm text-dark-400">
              Maximum file size: 500MB per file
            </p>
          </div>
        </div>
        
        <!-- Uploading Files -->
        <div v-if="uploadingFiles.length" class="space-y-4">
          <h3 class="text-lg font-semibold text-dark-900">Uploading Files</h3>
          <div class="space-y-3">
            <div 
              v-for="file in uploadingFiles" 
              :key="file.id"
              class="bg-white rounded-lg p-4 shadow-sm border border-gray-200"
            >
              <div class="flex items-center justify-between mb-2">
                <div class="flex items-center space-x-3">
                  <div class="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                    <svg class="w-5 h-5 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19V6l12-3v13M9 19c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2zm12-3c0 1.105-.895 2-2 2s-2-.895-2-2 .895-2 2-2 2 .895 2 2z"></path>
                    </svg>
                  </div>
                  <div>
                    <p class="font-medium text-dark-900">{{ file.name }}</p>
                    <p class="text-sm text-dark-500">{{ formatFileSize(file.size) }}</p>
                  </div>
                </div>
                <button 
                  @click="removeFile(file.id)"
                  class="text-red-500 hover:text-red-600 transition-colors"
                >
                  <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                  </svg>
                </button>
              </div>
              <div class="w-full bg-gray-200 rounded-full h-2">
                <div 
                  class="bg-primary-500 h-2 rounded-full transition-all duration-300"
                  :style="{ width: file.progress + '%' }"
                ></div>
              </div>
              <p class="text-sm text-dark-500 mt-1">{{ file.progress }}% complete</p>
            </div>
          </div>
        </div>
        
        <!-- Uploaded Files -->
        <div v-if="uploadedFiles.length && !uploadingFiles.length" class="space-y-4">
          <div class="flex items-center justify-between">
            <h3 class="text-lg font-semibold text-dark-900">
              Successfully Uploaded ({{ uploadedFiles.length }})
            </h3>
            <button 
              @click="clearUploaded"
              class="text-primary-500 hover:text-primary-600 font-medium"
            >
              Clear All
            </button>
          </div>
          <div class="grid grid-cols-1 md:grid-cols-2 gap-3">
            <div 
              v-for="file in uploadedFiles" 
              :key="file.id"
              class="bg-white rounded-lg p-4 shadow-sm border border-gray-200 flex items-center space-x-3"
            >
              <div class="w-10 h-10 bg-green-100 rounded-lg flex items-center justify-center">
                <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
                </svg>
              </div>
              <div class="flex-1">
                <p class="font-medium text-dark-900">{{ file.name }}</p>
                <p class="text-sm text-dark-500">{{ formatFileSize(file.size) }}</p>
              </div>
            </div>
          </div>
          <button 
            @click="resetUpload"
            class="btn-primary mx-auto"
          >
            Upload More Files
          </button>
        </div>
        
        <!-- Success Message -->
        <div v-if="successMessage" class="mt-4 p-4 bg-green-50 border border-green-200 rounded-lg">
          <div class="flex items-center space-x-2">
            <svg class="w-5 h-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="text-green-700">{{ successMessage }}</p>
          </div>
        </div>
        
        <!-- Error Message -->
        <div v-if="errorMessage" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <div class="flex items-center space-x-2">
            <svg class="w-5 h-5 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
            </svg>
            <p class="text-red-700">{{ errorMessage }}</p>
          </div>
        </div>
        
        <!-- Hidden File Input -->
        <input
          ref="fileInput"
          type="file"
          multiple
          accept=".mp3,.mp4,.wav,.m4a,.mov,.avi,.flac,.aac,.webm,.mkv,.wmv,.mpeg,.mpg"
          @change="handleFileSelect"
          class="hidden"
        />
      </div>
      
      <!-- Upload Button -->
      <div v-if="uploadingFiles.length" class="text-center mt-6">
        <button 
          @click="uploadFiles"
          :disabled="isUploading"
          class="btn-primary text-lg px-8 py-3"
          :class="{ 'opacity-50 cursor-not-allowed': isUploading }"
        >
          <svg v-if="isUploading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isUploading ? 'Uploading...' : `Upload ${uploadingFiles.length} File${uploadingFiles.length !== 1 ? 's' : ''}` }}
        </button>
      </div>
    </div>
  </section>
</template>

<script>
export default {
  name: 'UploadSection',
  data() {
    return {
      isDragging: false,
      dragCounter: 0,
      uploadingFiles: [],
      uploadedFiles: [],
      isUploading: false,
      errorMessage: '',
      successMessage: '',
      hasError: false,
      hasSuccess: false,
      nextFileId: 1,
      allowedTypes: [
        'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/m4a', 'audio/flac', 'audio/aac',
        'video/mp4', 'video/mov', 'video/avi', 'video/webm', 'video/mkv', 'video/wmv',
        'video/mpeg', 'video/mpg'
      ],
      maxFileSize: 500 * 1024 * 1024, // 500MB
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    }
  },
  methods: {
    handleDragEnter(e) {
      e.preventDefault()
      this.dragCounter++
      this.isDragging = true
    },
    
    handleDragLeave(e) {
      e.preventDefault()
      this.dragCounter--
      if (this.dragCounter === 0) {
        this.isDragging = false
      }
    },
    
    handleDragOver(e) {
      e.preventDefault()
    },
    
    handleDrop(e) {
      e.preventDefault()
      this.isDragging = false
      this.dragCounter = 0
      
      const files = Array.from(e.dataTransfer.files)
      this.processFiles(files)
    },
    
    triggerFileInput() {
      this.$refs.fileInput.click()
    },
    
    handleFileSelect(e) {
      const files = Array.from(e.target.files)
      this.processFiles(files)
      // Reset input
      e.target.value = ''
    },
    
    processFiles(files) {
      this.clearError()
      
      const validFiles = []
      const errors = []
      
      files.forEach(file => {
        // Check file type
        if (!this.allowedTypes.includes(file.type) && !this.isValidFileExtension(file.name)) {
          errors.push(`${file.name} is not a supported media file`)
          return
        }
        
        // Check file size
        if (file.size > this.maxFileSize) {
          errors.push(`${file.name} exceeds the maximum file size of 500MB`)
          return
        }
        
        // Check for duplicates
        if (this.uploadingFiles.some(f => f.name === file.name && f.size === file.size)) {
          errors.push(`${file.name} is already in the upload queue`)
          return
        }
        
        validFiles.push(file)
      })
      
      if (errors.length > 0) {
        this.showError(errors.join('; '))
        return
      }
      
      // Add valid files to upload queue
      validFiles.forEach(file => {
        this.uploadingFiles.push({
          id: this.nextFileId++,
          name: file.name,
          size: file.size,
          type: file.type,
          file: file,
          progress: 0
        })
      })
    },
    
    isValidFileExtension(filename) {
      const validExtensions = ['.mp3', '.mp4', '.wav', '.m4a', '.mov', '.avi', '.flac', '.aac', '.webm', '.mkv', '.wmv', '.mpeg', '.mpg']
      return validExtensions.some(ext => filename.toLowerCase().endsWith(ext))
    },
    
    removeFile(fileId) {
      this.uploadingFiles = this.uploadingFiles.filter(f => f.id !== fileId)
      this.clearError()
    },
    
    async uploadFiles() {
      if (this.uploadingFiles.length === 0) return
      
      this.isUploading = true
      this.clearError()
      
      try {
        // Upload files with progress tracking using XMLHttpRequest
        const result = await this.uploadFilesWithProgress()
        
        // Move successfully uploaded files to uploaded
        const successfulFiles = this.uploadingFiles.filter((fileObj, index) => 
          index < result.file_details.length
        )
        
        this.uploadedFiles.push(...successfulFiles.map((fileObj, index) => ({
          ...fileObj,
          serverResponse: result.file_details[index]
        })))
        
        // Clear uploading files
        this.uploadingFiles = []
        
        // Show success message and redirect to recordings
        if (result.failed_uploads > 0) {
          this.showError(`${result.successful_uploads} files uploaded successfully, ${result.failed_uploads} failed`)
        } else {
          // Show success notification
          this.showSuccessMessage(`${result.successful_uploads} file(s) uploaded successfully! Redirecting to recordings...`)
        }
        
        // Redirect to recordings page after a short delay to show success
        setTimeout(() => {
          this.$router.push('/recordings')
        }, 2000)
        
      } catch (error) {
        console.error('Upload error:', error)
        this.showError(error.message || 'Upload failed. Please try again.')
        
        // Reset progress for failed files
        this.uploadingFiles.forEach(fileObj => {
          fileObj.progress = 0
        })
      } finally {
        this.isUploading = false
      }
    },
    
    async uploadFilesWithProgress() {
      return new Promise((resolve, reject) => {
        const formData = new FormData()
        
        // Add all files to FormData
        this.uploadingFiles.forEach(fileObj => {
          formData.append('files', fileObj.file)
        })
        
        const xhr = new XMLHttpRequest()
        
        // Track upload progress
        xhr.upload.addEventListener('progress', (e) => {
          if (e.lengthComputable) {
            const overallProgress = Math.round((e.loaded / e.total) * 100)
            
            // Update progress for all files proportionally
            this.uploadingFiles.forEach(fileObj => {
              fileObj.progress = overallProgress
            })
          }
        })
        
        xhr.addEventListener('load', () => {
          if (xhr.status >= 200 && xhr.status < 300) {
            try {
              const result = JSON.parse(xhr.responseText)
              resolve(result)
            } catch (e) {
              reject(new Error('Invalid response format'))
            }
          } else {
            try {
              const errorData = JSON.parse(xhr.responseText)
              reject(new Error(errorData.detail || 'Upload failed'))
            } catch (e) {
              reject(new Error('Upload failed'))
            }
          }
        })
        
        xhr.addEventListener('error', () => {
          reject(new Error('Network error occurred'))
        })
        
        xhr.addEventListener('timeout', () => {
          reject(new Error('Upload timeout'))
        })
        
        // Set timeout to 5 minutes for large files
        xhr.timeout = 300000
        
        xhr.open('POST', `${this.apiBaseUrl}/api/v1/upload-multiple`)
        xhr.send(formData)
      })
    },
    
    async uploadSingleFile(fileObj) {
      try {
        // Create FormData for single file upload
        const formData = new FormData()
        formData.append('file', fileObj.file)
        
        // Track upload progress if supported
        return new Promise((resolve, reject) => {
          const xhr = new XMLHttpRequest()
          
          // Track upload progress
          xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
              fileObj.progress = Math.round((e.loaded / e.total) * 100)
            }
          })
          
          xhr.addEventListener('load', () => {
            if (xhr.status >= 200 && xhr.status < 300) {
              resolve(JSON.parse(xhr.responseText))
            } else {
              reject(new Error('Upload failed'))
            }
          })
          
          xhr.addEventListener('error', () => {
            reject(new Error('Upload failed'))
          })
          
          xhr.open('POST', `${this.apiBaseUrl}/api/v1/upload`)
          xhr.send(formData)
        })
      } catch (error) {
        throw error
      }
    },
    
    formatFileSize(bytes) {
      if (bytes === 0) return '0 Bytes'
      const k = 1024
      const sizes = ['Bytes', 'KB', 'MB', 'GB']
      const i = Math.floor(Math.log(bytes) / Math.log(k))
      return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i]
    },
    
        showError(message) {
      this.errorMessage = message
      this.hasError = true
      this.hasSuccess = false
      setTimeout(() => {
        this.clearError()
      }, 5000)
    },
    
    showSuccessMessage(message) {
      this.successMessage = message
      this.hasSuccess = true
      this.hasError = false
      setTimeout(() => {
        this.clearSuccess()
      }, 3000)
    },

    clearError() {
      this.errorMessage = ''
      this.hasError = false
    },
    
    clearSuccess() {
      this.successMessage = ''
      this.hasSuccess = false
    },
    
    clearUploaded() {
      this.uploadedFiles = []
    },
    
    resetUpload() {
      this.uploadedFiles = []
      this.uploadingFiles = []
      this.clearError()
    }
  }
}
</script> 