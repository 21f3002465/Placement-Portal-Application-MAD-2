<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
import CreateDrive from './CreateDrive.vue';

const router = useRouter();

const ongoingdrives = ref([])
const showCreateDriveForm = ref(false)
const studentapplications = ref([])
const view_applic = ref('')
const comprofile = ref([])

// View Profile
async function viewprofile() {
    try {
        const token = sessionStorage.getItem('token')
        console.log(token)
        const response = await fetch('http://127.0.0.1:5000/api/company/profile', {
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
onMounted(async () => {
    const profil = await viewprofile()
    if(profil){
        // Assign backend data to the reactive variable
        comprofile.value = profil;
    }
})



// View Created Placement Drives
async function viewsongoingdrives() {
    try {
        const token = sessionStorage.getItem('token')
        console.log(token)
        const response = await fetch('http://127.0.0.1:5000/api/company/ongoingdrives', {
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
    const ong_drive = await viewsongoingdrives()
    if(ong_drive){
        // Assign backend data to the reactive variable
        ongoingdrives.value = ong_drive;
    }
})


// View Student Applications
async function viewstudentsapplications() {
    try {
        const token = sessionStorage.getItem('token')
        console.log(token)
        const response = await fetch('http://127.0.0.1:5000/api/company/applications', {
            method:'GET',
            headers: {'Content-Type':'application/json',
            'Authentication-Token': token
            }
        });
        
        if (!response.ok) {
            if (response.status === 401 || response.status === 403) {
                sessionStorage.removeItem('token')
                sessionStorage.removeItem('UserRole')
                router.push('/login')
            }
            return null
        }

        const data = await response.json();
        return data;
    } catch (error){
        console.log(error)
        return null
    }
}

// Refresh the applications data in the dropdown options list
async function refreshApplications() {
    const applic = await viewstudentsapplications()
    if(applic){
        // Assign backend data to the reactive variable
        view_applic.value = applic;
        studentapplications.value = applic;
    }
}

// Trigger and fetch automatically when the page loads
onMounted(refreshApplications)


// Delete placement drive
async function delete_drive(drive_id){
    try {
        const token = sessionStorage.getItem('token')
        const response = await fetch('http://127.0.0.1:5000/api/company/delete_drive', { 
            method:'DELETE',
            headers:{
                'Content-Type':'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({
                drive_id: drive_id,
            })
        })
        
        if (response.ok) {
            const data = await response.json()
            // Remove approved drive from pending list in UI
            ongoingdrives.value = ongoingdrives.value.filter(drive => drive.id !== drive_id)
            return data;
        } else {
            console.error('Failed to approve drive:', response.statusText)
        }
    } catch(error){
        console.error(error);
    }
}

// Approve students/ Reject students/ shortlist students
async function approve_student(application_id, application_status){
    try{
        const token = sessionStorage.getItem('token')
        const response = await fetch('http://127.0.0.1:5000/api/company/approveapplication', { 
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({
                application_id: application_id,
                application_status: application_status,
            })
        })
        if(response.ok){
            const data = await response.json()
            return data
        }
    }
    catch(error){
        console.error(error)
        return null
    }
}



</script>


<template>

<div class="card">
      <h5 class="card-header">Profile</h5>
  <div class="card-body">
    <div class="row g-7">
      <div class="col-auto">
        <ul class="list-group">
            <h6 class="card-header">
                <span> Name </span>
                <span> Contact Number </span>
                <span> Address </span>
                <span> Website </span>
            </h6>
            <li v-for= "company in comprofile" :key="company.id" class="list-group-item d-flex justify-content-between align-items-center gap-5">
                <span>{{ company.name }} </span>
                <span>{{ company.contact_number }}</span>
                <span>{{ company.address }}</span>
                <span>{{ company.website }}</span>
            </li>
        </ul>
    </div>
</div>
</div>
</div>

  <div class="card">
    <div class="card-body">
      <div class="d-flex justify-content-between align-items-center mb-4">
        <h4 class="mb-0">Ongoing Drives</h4>
        <button class="btn btn-outline-success" v-if="!showCreateDriveForm" @click.prevent="showCreateDriveForm=true">Create Drives</button>
      </div>
      
<div class="card">
      <h5 class="card-header">Ongoing Drives</h5>
   
  <div class="card-body">
    <div class="row g-7">
      <div class="col-auto">
        <ul class="list-group">
               <h6 class="card-header">
                <span> Name of Drive </span>
                <span> Job Title </span>
                <span> Job Description </span>
                <span> Type </span>
                <span> Salary </span>
                <span> Location </span>
                <span> Eligibility </span>
                <span> Posted On </span>
                <span> Deadline </span>
      </h6>
            <li v-for= "drive in ongoingdrives" :key="drive.id" class="list-group-item d-flex justify-content-between align-items-center gap-5">
                <span>{{ drive.drive_name }} </span>
                <span> {{ drive.title }} </span>
                <span>{{ drive.description }}</span>
                <span> {{ drive.type }} </span>
                <span> {{ drive.salary }} </span>
                <span> {{ drive.location }} </span>
                <span> {{ drive.eligibility }} </span>
                <span> {{ drive.posted_on }} </span>
                <span> {{ drive.deadline }} </span>
                    <form class="d-flex">
                <button class="btn btn-danger" @click.prevent="delete_drive(drive.id)">Delete</button>
                </form>
            </li>
        </ul>
    </div>
</div>
</div>
</div>

<!-- Create Drive Form -->
<CreateDrive v-if='showCreateDriveForm' @close="showCreateDriveForm=false" @created="refreshApplications"/>


    </div>
  </div>

  <!-- View Student Applications -->
<div class="card mt-3">
      <h5 class="card-header">Student Applications</h5>
  <div class="card-body">
        <ul class="list-group">
            <li v-for="app in studentapplications" :key="app.id" class="list-group-item d-flex justify-content-between align-items-center">
                <div>
                  <strong>Application #{{ app.id }}</strong>
                  <span class="ms-2 text-muted">Student ID: {{ app.student_id }} ; Drive ID: {{ app.drive_id }}</span>
                  
                </div>
                <span class="btn btn-success" @click.prevent="approve_student(app.id, 'approve')">Approve</span>
                  <button class="btn btn-danger" @click.prevent="approve_student(app.id, 'reject')">Reject</button>
                  <button class="btn btn-info" @click.prevent="approve_student(app.id, 'shortlist')">Shortlist</button>
                  
                <span class="badge" :class="{
                  'bg-success': app.application_status === 'approved',
                  'bg-danger': app.application_status === 'rejected',
                  'bg-warning text-dark': app.application_status === 'shortlisted',
                  'bg-secondary': !app.application_status || app.application_status === 'pending'
                }">{{ app.application_status || app.status || 'pending' }}</span>
            </li>
        </ul>
</div>
</div>
</template>
