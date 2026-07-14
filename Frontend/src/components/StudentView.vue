<script setup>
import {ref, onMounted} from 'vue'
import { useRouter } from 'vue-router'

const viewdrives = ref([])
const my_applications = ref([])

async function viewdrive () {
    try {
        const token = sessionStorage.getItem('token')
        console.log(token)
        const response = await fetch('http://127.0.0.1:5000/api/students/viewdrives', {
            method:'GET',
            headers: {'Content-Type':'application/json',
            'Authentication-Token': token
            }
            
        });
        // Extracting the data from the response
        const data = await response.json();

        // Return data for the vue component to use it
        return data;
    } catch (error){
        console.log(error)

    }
}

// Trigger and fetch automatically when the page loads
onMounted(async () => {
    const drives = await viewdrive()
    if(drives){
        viewdrives.value = drives;
    }
})

// Student apply drives
async function apply_drive(drive_id) {
    try {
        const token = sessionStorage.getItem('token')
        const response = await fetch('http://127.0.0.1:5000/api/students/apply/${drive_id}', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            }
        })

        const data = await response.json().catch(() => ({}))
        if (response.ok) {
            viewdrives.value = viewdrives.value.filter(drive => drive.id !== drive_id)
            alert(data.message || 'Application submitted successfully')
        } else {
            alert(data.message || 'Unable to apply for this drive')
        }
    } catch (error) {
        console.log(error)
    }
}

// Student upload resume
const file = ref(null)

// When item is selected in the browser
function pickfile(event) {
    file.value = event.target.files[0]
}

// File to be sent to backend
async function uploadfile() {
    if (!file.value) {
        alert('Please select a resume file first')
        return
    }

    const formdata = new FormData()
    formdata.append('resume', file.value)

    const token = sessionStorage.getItem('token')
    const response = await fetch('http://127.0.0.1:5000/api/student/resume', {
        method: 'POST',
        headers: {
            'Authentication-Token': token
        },
        body: formdata
    })

    const data = await response.json().catch(() => ({}))
    if (response.ok) {
        alert(data.message || 'Resume uploaded successfully')
    } else {
        alert(data.message || 'Resume upload failed')
    }
}


// My Applications
async function myapplications() {
    try {
        const token = sessionStorage.getItem('token')
        const response = await fetch('http://127.0.0.1:5000/api/student/search', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authentication-Token': token
            }
        })

        const data = await response.json().catch(() => ({}))
        if (response.ok) {
            return data
        } else {
            alert(data.message || 'Unable to fetch my applications')
            return []
        }
    } catch (error) {
        console.log(error)
        return []
    }
}

onMounted(async () => {
    const apps = await myapplications()
    if(apps){
        my_applications.value = apps;
    }
})
</script>




<template>
    <!-- Form for Resume to be uploaded by student -->
<div class="card">
      <h5 class="card-header">Upload Resume</h5>
  <div class="card-body">
    <div class="row g-7"> 
      <div class="col-auto">
        <form @submit.prevent="uploadfile">
            <input type="file" @change="pickfile">
            <button type="submit">Upload</button>
        </form>
    </div>
</div>
</div>
</div>

<div class="card">
      <h5 class="card-header">Ongoing Drives</h5>
  <div class="card-body">
    <div class="row g-7">
      <div class="col-auto">
        <ul class="list-group">
            <li v-for= "drive in viewdrives" :key="drive.id" class="list-group-item d-flex justify-content-between align-items-center gap-5">
                <span>{{ drive.drive_name }} ({{ drive.job_title }})</span>
                    <form class="d-flex">
                 <button type="button" @click="apply_drive(drive.id)" class="btn btn-success">Apply</button>
                </form>
            </li>
        </ul>
    </div>
</div>
</div>
</div>

<div class="card">
      <h5 class="card-header">My Applications</h5>
  <div class="card-body">
    <div class="row g-7">
      <div class="col-auto">
        <ul class="list-group">
            <h6 class="card-header">
                <span> Application ID </span>
                <span> Drive ID </span>
                <span> Applied On </span>
                <span> Application Status </span>
            </h6>
            <li v-for= "app in my_applications" :key="app.id" class="list-group-item d-flex justify-content-between align-items-center gap-5">
                <span>{{ app.id }}</span>
                <span>({{ app.drive_id }})</span>
                <span> {{ app.applied_on }}</span>
                <span>{{ app.application_status }}</span>
            </li>
        </ul>
    </div>
</div>
</div>
</div>


</template>

<style>
</style>