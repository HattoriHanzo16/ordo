<template>
  <div class="min-h-screen bg-secondary-50">
    <NavBar />
    
    <main class="container mx-auto px-4 py-8">
      <div class="max-w-4xl mx-auto">
        <!-- Page Header -->
        <div class="mb-8">
          <h1 class="text-3xl font-bold text-dark-900 mb-2">Settings</h1>
          <p class="text-dark-600">Configure labeling rules for automatic meeting categorization</p>
        </div>

        <!-- Labeling Rules Section -->
        <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
          <div class="flex items-center justify-between mb-6">
            <div>
              <h2 class="text-xl font-semibold text-dark-900 mb-2">Labeling Rules</h2>
              <p class="text-dark-600">Define rules for AI to automatically categorize your meetings</p>
            </div>
            <button
              @click="showCreateForm = true"
              class="btn-primary flex items-center"
            >
              <svg class="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6"></path>
              </svg>
              Add Rule
            </button>
          </div>

          <!-- Create/Edit Form -->
          <div v-if="showCreateForm || editingRule" class="mb-6 p-4 bg-gray-50 rounded-lg border">
            <h3 class="text-lg font-medium text-dark-900 mb-4">
              {{ editingRule ? 'Edit Rule' : 'Create New Rule' }}
            </h3>
            
            <form @submit.prevent="saveRule" class="space-y-4">
              <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label class="block text-sm font-medium text-dark-700 mb-2">Label Name</label>
                  <input
                    v-model="ruleForm.label_name"
                    type="text"
                    placeholder="e.g., Effective, Boring, Too Long"
                    class="input-field"
                    required
                  />
                </div>
                <div>
                  <label class="block text-sm font-medium text-dark-700 mb-2">Color</label>
                  <div class="flex items-center space-x-2">
                    <input
                      v-model="ruleForm.label_color"
                      type="color"
                      class="w-12 h-10 border border-gray-300 rounded cursor-pointer"
                    />
                    <input
                      v-model="ruleForm.label_color"
                      type="text"
                      placeholder="#3B82F6"
                      class="input-field flex-1"
                      pattern="^#[0-9A-Fa-f]{6}$"
                      required
                    />
                  </div>
                </div>
              </div>
              
              <div>
                <label class="block text-sm font-medium text-dark-700 mb-2">Rule Description</label>
                <textarea
                  v-model="ruleForm.rule_description"
                  rows="4"
                  placeholder="Describe when this label should be applied. E.g., 'Apply this label to meetings that are longer than 60 minutes with few action items' or 'Apply this label to meetings with clear outcomes and specific action items assigned to team members'"
                  class="input-field resize-none"
                  required
                ></textarea>
                <p class="text-xs text-dark-500 mt-1">Be specific about criteria. The AI will use this description to decide when to apply the label.</p>
              </div>
              
              <div class="flex items-center space-x-3">
                <input
                  v-model="ruleForm.is_active"
                  type="checkbox"
                  id="is_active"
                  class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
                />
                <label for="is_active" class="text-sm text-dark-700">Active (apply to new recordings)</label>
              </div>
              
              <div class="flex items-center space-x-3">
                <button type="submit" class="btn-primary" :disabled="saving">
                  {{ saving ? 'Saving...' : (editingRule ? 'Update Rule' : 'Create Rule') }}
                </button>
                <button type="button" @click="cancelEdit" class="btn-secondary">
                  Cancel
                </button>
              </div>
            </form>
          </div>

          <!-- Rules List -->
          <div v-if="loading" class="text-center py-8">
            <svg class="animate-spin h-8 w-8 text-primary-500 mx-auto mb-4" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p class="text-dark-600">Loading rules...</p>
          </div>

          <div v-else-if="rules.length === 0" class="text-center py-8">
            <div class="w-16 h-16 bg-gray-100 rounded-full flex items-center justify-center mx-auto mb-4">
              <svg class="w-8 h-8 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z"></path>
              </svg>
            </div>
            <h3 class="text-lg font-semibold text-dark-900 mb-2">No labeling rules yet</h3>
            <p class="text-dark-600 mb-4">Create your first rule to automatically categorize meetings</p>
            <button @click="showCreateForm = true" class="btn-primary">
              Create First Rule
            </button>
          </div>

          <div v-else class="space-y-4">
            <div
              v-for="rule in rules"
              :key="rule.id"
              class="p-4 border border-gray-200 rounded-lg hover:border-gray-300 transition-colors"
            >
              <div class="flex items-start justify-between">
                <div class="flex-1">
                  <div class="flex items-center space-x-3 mb-2">
                    <span
                      class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium text-white"
                      :style="{ backgroundColor: rule.label_color }"
                    >
                      {{ rule.label_name }}
                    </span>
                    <span
                      v-if="!rule.is_active"
                      class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-gray-100 text-gray-600"
                    >
                      Inactive
                    </span>
                  </div>
                  <p class="text-dark-700 mb-2">{{ rule.rule_description }}</p>
                  <p class="text-xs text-dark-500">
                    Created {{ formatDate(rule.created_at) }}
                    <span v-if="rule.updated_at !== rule.created_at">
                      • Updated {{ formatDate(rule.updated_at) }}
                    </span>
                  </p>
                </div>
                <div class="flex items-center space-x-2 ml-4">
                  <button
                    @click="startEdit(rule)"
                    class="text-gray-400 hover:text-primary-500 transition-colors"
                    title="Edit rule"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"></path>
                    </svg>
                  </button>
                  <button
                    @click="deleteRule(rule.id)"
                    class="text-gray-400 hover:text-red-500 transition-colors"
                    title="Delete rule"
                  >
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path>
                    </svg>
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import NavBar from './NavBar.vue'

export default {
  name: 'SettingsPage',
  components: {
    NavBar
  },
  data() {
    return {
      rules: [],
      loading: false,
      saving: false,
      showCreateForm: false,
      editingRule: null,
      ruleForm: {
        label_name: '',
        label_color: '#3B82F6',
        rule_description: '',
        is_active: true
      },
      apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    }
  },
  mounted() {
    this.fetchRules()
  },
  methods: {
    async fetchRules() {
      this.loading = true
      try {
        const response = await fetch(`${this.apiBaseUrl}/api/v1/labeling/`)
        if (!response.ok) throw new Error('Failed to fetch rules')
        
        this.rules = await response.json()
      } catch (error) {
        console.error('Error fetching rules:', error)
      } finally {
        this.loading = false
      }
    },
    
    async saveRule() {
      this.saving = true
      try {
        const url = this.editingRule 
          ? `${this.apiBaseUrl}/api/v1/labeling/${this.editingRule.id}`
          : `${this.apiBaseUrl}/api/v1/labeling/`
        
        const method = this.editingRule ? 'PUT' : 'POST'
        
        const response = await fetch(url, {
          method,
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(this.ruleForm)
        })
        
        if (!response.ok) throw new Error('Failed to save rule')
        
        await this.fetchRules()
        this.cancelEdit()
      } catch (error) {
        console.error('Error saving rule:', error)
      } finally {
        this.saving = false
      }
    },
    
    async deleteRule(ruleId) {
      if (!confirm('Are you sure you want to delete this rule? This action cannot be undone.')) {
        return
      }
      
      try {
        const response = await fetch(`${this.apiBaseUrl}/api/v1/labeling/${ruleId}`, {
          method: 'DELETE'
        })
        
        if (!response.ok) throw new Error('Failed to delete rule')
        
        await this.fetchRules()
      } catch (error) {
        console.error('Error deleting rule:', error)
      }
    },
    
    startEdit(rule) {
      this.editingRule = rule
      this.ruleForm = {
        label_name: rule.label_name,
        label_color: rule.label_color,
        rule_description: rule.rule_description,
        is_active: rule.is_active
      }
      this.showCreateForm = false
    },
    
    cancelEdit() {
      this.showCreateForm = false
      this.editingRule = null
      this.ruleForm = {
        label_name: '',
        label_color: '#3B82F6',
        rule_description: '',
        is_active: true
      }
    },
    
    formatDate(dateString) {
      return new Date(dateString).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
      })
    }
  }
}
</script> 