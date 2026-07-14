<script setup>
import {ref} from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
// To show error messages to user
const error_message = ref('')
const password = ref('')

const router = useRouter()

async function handlelogin() {
    error_message.value = ''
    console.log(username.value, password.value)
    
    try {
        const response = await fetch('http://127.0.0.1:5000/api/Login', {
            method:'POST',
            headers: {'Content-Type':'application/json'},
        body: JSON.stringify({
            username: username.value,
            password: password.value
        })
    })
     //1. backend response to javascript
    const data = await response.json()

    if (response.ok && data.user && data.user.role) {
        // Save the auth token
        sessionStorage.setItem('token', data.auth_token)
        //2. Save the role of the user excatly as read in Dashboard
        sessionStorage.setItem('UserRole', data.user.role)
        // 3. Send the user to the single dashboard page
        console.log("Redirection is starting right now...")
        router.push('/dashboard')
    } else {
        error_message.value = data.message || 'Invalid username/ password'
    }
   
} catch (error){
    console.log(error)
    error_message.value = 'Cannot connect to server, try agin later'
    }
}

</script>


<template>
<div v-if="error_message", class="alert-box">
    <div class="flash-card alert-danger text-center">
        {{ error_message }}
    </div>
    
</div>
<div class="container-fluid row justify-content-center mt-5">
     <div class="col-md-4">
             <div class="text-center"><h4>Login</h4></div>
             <div class="card-body">
                <form @submit.prevent="handlelogin"> 
                     <div class="mb-3">
                        <label for="username">Username</label>
                          <input type="text" class="form-control" id="username" v-model="username">
                     </div>
                     <div class="mb-3">
                        <label for="inputPassword5">Password</label>
                        <input type="password" id="inputPassword5" class="form-control" aria-describedby="passwordHelpBlock" v-model="password">
                          </div>
                    <button type='submit' class="btn btn-primary w-100">Sign In</button>
            </form>
            <div class="mt-3 text-center">
                <router-link to="/register/student">Do not have an account? Register(Student)</router-link>
                
            </div>
             <div class="mt-3 text-center">
                <router-link to="/register/company">Do not have an account? Register(Company)</router-link>
             </div>
        </div>
    </div>
</div>
</template>

<style>
</style>