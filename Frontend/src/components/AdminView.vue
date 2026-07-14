<script setup>
import { onMounted, ref } from 'vue';
import { useRouter } from 'vue-router';
const router = useRouter();

// A reactive variable that holds the list
const companies = ref([])
const students = ref([])
const pendingcompanies = ref([])
const studentapplications = ref([])
const ongoingdrives = ref([])
const pendingdrives = ref([])


// To save data to ref from backend
async function viewcompanies() {
    try {
        const token = sessionStorage.getItem('token')
        console.log(token)
        const response = await fetch('http://127.0.0.1:5000/api/company', {
            method:'GET',
            headers: {'Content-Type':'application/json',
            // 'Authentication-Token': token
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
    const result = await viewcompanies()
    if(result){
        // Assign backend data to the reactive variable
        companies.value = result;
    }
})

// Students
async function viewstudents() {
    try {
        const token = sessionStorage.getItem('token')
        console.log(token)
        const response = await fetch('http://127.0.0.1:5000/api/students', {
            method:'GET',
            headers: {'Content-Type':'application/json',
            // 'Authentication-Token': token
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
    const stud = await viewstudents()
    if(stud){
        // Assign backend data to the reactive variable
        students.value = stud;
    }
})

// View Pending Companies
async function viewpendingcompanies() {
    try {
        const token = sessionStorage.getItem('token')
        console.log(token)
        const response = await fetch('http://127.0.0.1:5000/api/admin/pendingcompany', {
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
    const com = await viewpendingcompanies()
    if(com){
        // Assign backend data to the reactive variable
        pendingcompanies.value = com;
    }
})

// Approve companies
async function approve_company(company_id){
    try {
        const token = sessionStorage.getItem('token')
        const response = await fetch('http://127.0.0.1:5000/api/admin/approvecompany', { 
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({
                company_id: company_id,
                action: 'approve'
            })
        })
        
        if (response.ok) {
            const data = await response.json()
            // Remove approved company from pending list in UI
            pendingcompanies.value = pendingcompanies.value.filter(com => com.id !== company_id)
            return data;
        } else {
            console.error('Failed to approve company:', response.statusText)
        }
    } catch(error){
        console.error(error);
    }
}

// View student applications
async function viewstudentsapplications() {
    try {
        const token = sessionStorage.getItem('token')
        console.log(token)
        const response = await fetch('http://127.0.0.1:5000/api/student/applications', {
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
    const apps = await viewstudentsapplications()
    if(apps){
        studentapplications.value = apps;
    }
})

// View ongoing drives
async function viewsongoingdrives() {
    try {
        const token = sessionStorage.getItem('token')
        console.log(token)
        const response = await fetch('http://127.0.0.1:5000/api/admin/ongoingdrives', {
            method:'GET',
            headers: {'Content-Type':'application/json',
            // 'Authentication-Token': token
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



// Approve Drives
// View Pending Drives
async function viewpendingdrives() {
    try {
        const token = sessionStorage.getItem('token')
        console.log(token)
        const response = await fetch('http://127.0.0.1:5000/api/admin/pendingdrive', {
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
    const drive = await viewpendingdrives()
    if(drive){
        // Assign backend data to the reactive variable
        pendingdrives.value = drive;
    }
})

// Approve drives
async function approve_drive(drive_id){
    try {
        const token = sessionStorage.getItem('token')
        const response = await fetch('http://127.0.0.1:5000/api/admin/approvedrive', { 
            method:'POST',
            headers:{
                'Content-Type':'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({
                drive_id: drive_id,
                status: 'approve'
            })
        })
        
        if (response.ok) {
            const data = await response.json()
            // Remove approved drive from pending list in UI
            pendingdrives.value = pendingdrives.value.filter(drive => drive.id !== drive_id)
            return data;
        } else {
            console.error('Failed to approve drive:', response.statusText)
        }
    } catch(error){
        console.error(error);
    }
}

// Delete user
async function delete_user(id){
    try {
        const token = sessionStorage.getItem('token')
        const response = await fetch('http://127.0.0.1:5000/api/admin/deleteuser', { 
            method:'DELETE',
            headers:{
                'Content-Type':'application/json',
                'Authentication-Token': token
            },
            body: JSON.stringify({
                id: id,
            })
        })
        
        if (response.ok) {
            const data = await response.json()
            // Remove approved drive from pending list in UI
            companies.value = companies.value.filter(comp => comp.id !== id)
            students.value = students.value.filter(stud => stud.id !== id)
            return data;
        } else {
            console.error('Failed to delete user:', response.statusText)
        }
    } catch(error){
        console.error(error);
    }
}


</script>

<template>


<div class="card">
      <h5 class="card-header">Registered Companies</h5>
  <div class="card-body">
    <div class="row g-7">
      <div class="col-auto">
        <ul class="list-group">
            <li v-for= "company in companies" :key="company.id" class="list-group-item d-flex justify-content-between align-items-center gap-5">
                <span>{{ company.username }} ({{ company.email }})</span>
                    <form class="d-flex">
                  <button class="btn btn-danger" @click.prevent="delete_user(company.id)">Delete</button>
                </form>
            </li>
        </ul>
    </div>
</div>
</div>
</div>

<div class="card">
      <h5 class="card-header">Registered Students</h5>
  <div class="card-body">
    <div class="row g-7">
      <div class="col-auto">
        <ul class="list-group">
            <li v-for= "student in students" :key="student.id" class="list-group-item d-flex justify-content-between align-items-center gap-5">
                <span>{{ student.username }} ({{ student.email }})</span>
                    <form class="d-flex">
                 <button class="btn btn-danger" @click.prevent="delete_user(student.id)">Delete</button>
                </form>
            </li>
        </ul>
    </div>
</div>
</div>
</div>

<div class="card">
      <h5 class="card-header">Company Applications</h5>
  <div class="card-body">
    <div class="row g-7">
      <div class="col-auto">
        <ul class="list-group">
            <li v-for= "com in pendingcompanies" :key="com.id" class="list-group-item d-flex justify-content-between align-items-center gap-5">
                <span>{{ com.username }} ({{ com.email }})</span>
                    <form class="d-flex">
                <!--button com.id checks id and id is sent to backend with action approve and company is approved from backend and removed from pending list -->
                 <button class="btn btn-success" @click.prevent="approve_company(com.id)">Approve</button>
                </form>
            </li>
        </ul>
    </div>
</div>
</div>
</div>

<div class="card">
      <h5 class="card-header">Student Applications</h5>
  <div class="card-body">
    <div class="row g-7">
      <div class="col-auto">
        <ul class="list-group">
            <h6>
                <span>Student ID </span><span> (Drive ID)</span>
            </h6>
            <li v-for= "student in studentapplications" :key="student.id" class="list-group-item d-flex justify-content-between align-items-center gap-5">
                <span>{{ student.id }}</span>
                <span> ({{ student.drive_id }})</span>
                    <form class="d-flex">
                </form>
            </li>
        </ul>
    </div>
</div>
</div>
</div>

<div class="card">
      <h5 class="card-header">Pending Drive Approvals</h5>
  <div class="card-body">
    <div class="row g-7">
      <div class="col-auto">
        <ul class="list-group">
            <li v-for="drive in pendingdrives" :key="drive.id" class="list-group-item d-flex justify-content-between align-items-center gap-5">
                <span>{{ drive.drive_name }} ({{ drive.title }})</span>
                    <form class="d-flex">
                 <button class="btn btn-success" @click.prevent="approve_drive(drive.id)">Approve</button>
                </form>
            </li>
        </ul>
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
            <li v-for= "drive in ongoingdrives" :key="drive.id" class="list-group-item d-flex justify-content-between align-items-center gap-5">
                <span>{{ drive.drive_name }} ({{ drive.title }})</span>
                    <form class="d-flex">
                 <!-- <button class="btn btn-success" @click.prevent="approve_drive(drive.id)">Approve</button> -->
                </form>
            </li>
        </ul>
    </div>
</div>
</div>
</div>


</template>


<style>

</style>
