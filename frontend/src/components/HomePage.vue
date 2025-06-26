<template>
  <div class="min-h-screen bg-secondary-50">
    <!-- Navigation Bar -->
    <NavBar />
    
    <!-- Main Content -->
    <main class="container mx-auto px-4 py-8">
      <!-- Hero Section -->
      <div class="text-center mb-16 animate-fade-in">
        <!-- Hero Content with Integrated Dolphin -->
        <div class="flex items-center justify-center gap-4 mb-6">
          <h1 class="text-5xl font-bold text-dark-900">
            Upload your <span class="text-primary-500">meetings</span>
          </h1>
          <div class="animate-float">
            <div class="relative">
              <div class="w-16 h-16 bg-gradient-to-br from-primary-100 to-primary-200 rounded-full flex items-center justify-center shadow-lg">
                <img 
                  src="/logo.svg" 
                  alt="Ordo Dolphin" 
                  class="h-10 w-10 opacity-90"
                />
              </div>
              <!-- Subtle glow effect -->
              <div class="absolute inset-0 w-16 h-16 bg-primary-300 rounded-full blur-lg opacity-20 animate-pulse"></div>
            </div>
          </div>
        </div>
        
        <p class="text-xl text-dark-600 max-w-3xl mx-auto leading-relaxed mb-4">
          We analyze and transcribe them automatically
        </p>
        <p class="text-lg text-dark-500 max-w-2xl mx-auto">
          Transform your meeting recordings into searchable transcripts with intelligent insights. 
          Simply upload your audio or video files and let our AI do the rest.
        </p>
      </div>

      <!-- Performance Stats -->
      <div class="mb-16 animate-fade-in">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-4xl mx-auto">
          <div class="text-center">
            <div class="text-3xl font-bold text-primary-500 mb-2">⚡ &lt;5 min</div>
            <p class="text-dark-600">Average transcription time</p>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-primary-500 mb-2">99%</div>
            <p class="text-dark-600">Accuracy rate</p>
          </div>
          <div class="text-center">
            <div class="text-3xl font-bold text-primary-500 mb-2">50+</div>
            <p class="text-dark-600">Languages supported</p>
          </div>
        </div>
      </div>
      
      <!-- Upload Section -->
      <UploadSection />

      <!-- How It Works Section -->
      <section class="mt-20 mb-20 animate-slide-up">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-dark-900 mb-4">How It Works</h2>
          <p class="text-lg text-dark-600 max-w-2xl mx-auto">
            Get from raw recording to actionable insights in just three simple steps
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div class="text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-dark-900 mb-2">1. Upload</h3>
            <p class="text-dark-600">Drop your meeting recording - we support all major audio and video formats</p>
          </div>
          
          <div class="text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-dark-900 mb-2">2. AI Processing</h3>
            <p class="text-dark-600">Our AI transcribes, identifies speakers, and extracts key insights automatically</p>
          </div>
          
          <div class="text-center">
            <div class="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-primary-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <h3 class="text-xl font-semibold text-dark-900 mb-2">3. Get Results</h3>
            <p class="text-dark-600">Receive searchable transcripts, summaries, and action items ready to use</p>
          </div>
        </div>
      </section>

      <!-- Key Features Section -->
      <section class="mt-20 mb-20 animate-slide-up">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-dark-900 mb-4">Powerful Features</h2>
          <p class="text-lg text-dark-600 max-w-2xl mx-auto">
            Everything you need to make your meetings more productive and actionable
          </p>
        </div>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 max-w-6xl mx-auto">
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div class="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-blue-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-dark-900 mb-2">Speaker Identification</h3>
            <p class="text-dark-600">Automatically identify and label different speakers throughout your meeting</p>
          </div>
          
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div class="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-dark-900 mb-2">Smart Summaries</h3>
            <p class="text-dark-600">Get concise summaries with key points and important decisions highlighted</p>
          </div>
          
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div class="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-purple-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v6a2 2 0 002 2h6a2 2 0 002-2V7a2 2 0 00-2-2H9z"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5a2 2 0 012-2h2a2 2 0 012 2"></path>
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-dark-900 mb-2">Action Items</h3>
            <p class="text-dark-600">Automatically extract tasks, deadlines, and follow-ups from discussions</p>
          </div>
          
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div class="w-12 h-12 bg-yellow-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-yellow-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-dark-900 mb-2">Searchable Transcripts</h3>
            <p class="text-dark-600">Find any moment in your meeting instantly with powerful search capabilities</p>
          </div>
          
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div class="w-12 h-12 bg-red-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-dark-900 mb-2">Meeting Insights</h3>
            <p class="text-dark-600">Analyze talk time, sentiment, and engagement patterns for better meetings</p>
          </div>
          
          <div class="bg-white rounded-xl p-6 shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
            <div class="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
              <svg class="w-6 h-6 text-indigo-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5h12M9 3v2m1.048 9.5A18.022 18.022 0 016.412 9m6.088 9h7M11 21l5-10 5 10M12.751 5C11.783 10.77 8.07 15.61 3 18.129"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-dark-900 mb-2">Multi-Language</h3>
            <p class="text-dark-600">Support for 50+ languages with automatic language detection</p>
          </div>
        </div>
      </section>

      <!-- Sample Output Preview -->
      <section class="mt-20 mb-20 animate-slide-up">
        <div class="text-center mb-12">
          <h2 class="text-3xl font-bold text-dark-900 mb-4">See What You Get</h2>
          <p class="text-lg text-dark-600 max-w-2xl mx-auto">
            Here's a preview of the rich insights and transcripts you'll receive
          </p>
        </div>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 max-w-6xl mx-auto">
          <!-- Transcript Preview -->
          <div class="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
            <div class="flex items-center mb-4">
              <div class="w-3 h-3 bg-red-500 rounded-full mr-2"></div>
              <div class="w-3 h-3 bg-yellow-500 rounded-full mr-2"></div>
              <div class="w-3 h-3 bg-green-500 rounded-full mr-4"></div>
              <span class="text-sm text-dark-500 font-mono">transcript.txt</span>
            </div>
            <div class="space-y-3 text-sm">
              <div class="flex">
                <span class="text-blue-600 font-medium min-w-20">Sarah:</span>
                <span class="text-dark-700">Let's discuss the Q4 marketing budget. I think we need to allocate more resources to digital campaigns.</span>
              </div>
              <div class="flex">
                <span class="text-green-600 font-medium min-w-20">Mike:</span>  
                <span class="text-dark-700">Agreed. Based on our analytics, social media ROI has increased by 40% this quarter.</span>
              </div>
              <div class="flex">
                <span class="text-purple-600 font-medium min-w-20">Jenny:</span>
                <span class="text-dark-700">We should also consider influencer partnerships. Can we schedule a follow-up meeting for next Tuesday?</span>
              </div>
            </div>
          </div>
          
          <!-- Action Items & Summary -->
          <div class="space-y-6">
            <div class="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
              <h4 class="font-semibold text-dark-900 mb-3 flex items-center">
                <svg class="w-5 h-5 text-green-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                </svg>
                Action Items
              </h4>
              <ul class="space-y-2 text-sm">
                <li class="flex items-start">
                  <span class="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span>Schedule follow-up meeting for next Tuesday - Jenny</span>
                </li>
                <li class="flex items-start">
                  <span class="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span>Research influencer partnership costs - Mike</span>
                </li>
                <li class="flex items-start">
                  <span class="w-2 h-2 bg-primary-500 rounded-full mt-2 mr-3 flex-shrink-0"></span>
                  <span>Prepare Q4 budget proposal - Sarah</span>  
                </li>
              </ul>
            </div>
            
            <div class="bg-white rounded-xl p-6 shadow-lg border border-gray-100">
              <h4 class="font-semibold text-dark-900 mb-3 flex items-center">
                <svg class="w-5 h-5 text-blue-500 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
                </svg>
                Key Summary
              </h4>
              <p class="text-sm text-dark-700">
                Team discussed Q4 marketing budget allocation with focus on digital campaigns. 
                Social media ROI up 40%. Considering influencer partnerships. Follow-up meeting scheduled for next Tuesday.
              </p>
            </div>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'
import UploadSection from './UploadSection.vue'

export default {
  name: 'HomePage',
  components: {
    NavBar,
    UploadSection
  }
}
</script> 