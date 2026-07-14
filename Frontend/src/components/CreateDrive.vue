// Create Placement Drives
<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const emit = defineEmits(['created', 'close'])
const router = useRouter()
const drive_name = ref('')
const title = ref('')
const type = ref('')
const salary = ref()
const location = ref()
const description = ref()
const eligibility = ref()
const posted_date = ref()
const deadline = ref()

async function create_drive(){
      try {
        const token = sessionStorage.getItem('token')
        const response = await fetch('http://127.0.0.1:5000/api/company/createdrive', { 
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({
                "drive_name": drive_name.value,
                "title": title.value,
                "type": type.value,
                "salary": salary.value,
                "location": location.value,
                "description": description.value,
                "eligibility": eligibility.value,
                "posted_date": posted_date.value,
                "deadline": deadline.value
            })
        })
        
        if (response.ok) {
            const data = await response.json()
            emit('created')
            emit('close')
            router.push('/login')
            return data;
        } else {
            console.error('Failed to create drive:', response.statusText)
            return null
        }
    } catch(error){
        console.error(error);
    }
}

</script>

<template>
  <div class="card border border-primary-subtle shadow-sm mb-4">
    <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
      <h5 class="mb-0 text-white">Create Placement Drive</h5>
      <button type="button" class="btn-close btn-close-white" @click="emit('close')" aria-label="Close"></button>
    </div>
    <div class="card-body p-4">
      <form @submit.prevent="create_drive">
        <div class="row g-3">
          <!-- Drive Name & Job Title -->
          <div class="col-md-6">
            <label for="drive_name" class="form-label fw-semibold">Drive Name</label>
            <input type="text" class="form-control" id="drive_name" v-model="drive_name" placeholder="e.g. Google Summer Drive 2026" required>
          </div>
          <div class="col-md-6">
            <label for="title" class="form-label fw-semibold">Job Title</label>
            <input type="text" class="form-control" id="title" v-model="title" placeholder="e.g. Frontend Engineer" required>
          </div>
        </div>

          <!-- Type, Salary & Location -->
          <div class="col-md-4">
            <label for="type" class="form-label fw-semibold">Job Type</label>
            <select id="type" class="form-select" v-model="type" required>
              <option value="" disabled selected>Select job type...</option>
              <option value="Full-Time">Full-Time</option>
              <option value="Part-Time">Part-Time</option>
              <option value="Internship">Internship</option>
            </select>
                    </div>
          <div class="col-md-4">
            <label for="salary" class="form-label fw-semibold">Salary (CTC in LPA / Stipend)</label>
            <input type="number" class="form-control" id="salary" v-model="salary" placeholder="e.g. 15" required>
                     </div>
          <div class="col-md-4">
            <label for="location" class="form-label fw-semibold">Location</label>
            <input type="text" class="form-control" id="location" v-model="location" placeholder="e.g. Bangalore / Remote" required>
                    </div>

          <!-- Dates -->
          <div class="col-md-6">
            <label for="posted_date" class="form-label fw-semibold">Posted Date</label>
            <input type="text" class="form-control" id="posted_date" v-model="posted_date" required>
                     </div>
          <div class="col-md-6">
            <label for="deadline" class="form-label fw-semibold">Application Deadline</label>
            <input type="text" class="form-control" id="deadline" v-model="deadline" required>
                     </div>
                    <div class="mb-3">
                        <label>Description</label>
                          <input type="text" class="form-control" id="description" v-model="description">
                     </div>
                     <div class="mb-3">
                        <label>Eligibility</label>
                          <input type="text" class="form-control" id="eligibility" v-model="eligibility">
                     </div>
                    <button type='submit' class="btn btn-info w-100">Create</button>
          
            </form>
        </div>
    </div>
</template>


