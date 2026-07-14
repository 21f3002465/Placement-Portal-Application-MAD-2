<script setup>
import {ref} from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const email = ref('')
const password = ref('')
const role = ref('')
const name = ref('')
const contact_number = ref('')
const website = ref('')
const address = ref('')

const router = useRouter()
async function handleregister() {
        const response = await fetch('http://127.0.0.1:5000/api/Register/Company', {
            method:'POST',
            headers: {'Content-Type':'application/json'
        },
        body: JSON.stringify({
            username: username.value,
            password: password.value,
            email : email.value,
            role : 'company',
            name : name.value,
            address : address.value,
            contact_number :contact_number.value,
            website : website.value

        })
    })
    const data = await response.json()
    if (response.ok) {
        console.log("registation done")
        router.push('/login')
    }else{
        console.error(data.message)
    }
    }
</script>
<template>
       <div class="container-fluid row justify-content-center mt-5">
 
     <div class="form-group col-md-6">
          
             <div class="text-center"><h4>Registration Form</h4></div>
             <div class="card-body">
                <form @submit.prevent=handleregister>
                     <div class="mb-3">
                        <label>Username</label>
                        <input type="text" class="form-control" id = 'username' v-model="username">
                    </div>
                     <div class="mb-3">
                        <label>Email</label>
                          <input type="email" class="form-control" id="email" placeholder="name@example.com" v-model="email">
                     </div>
                     <div class="mb-3">
                        <label>Password</label>
                        <input type="password" id="password" class="form-control" aria-describedby="passwordHelpBlock" v-model="password">
                        <div id="passwordHelpBlock" class="form-text">
                            Your password must be 8-20 characters long, contain letters and numbers, and must not contain spaces, special characters, or emoji.
                        </div>
                    </div>
                    <div class="mb-3">
                        <label>Name</label>
                          <input type="text" class="form-control" id="name" v-model="name">
                     </div>
                     <div class="mb-3">
                        <label>Address</label>
                          <input type="text" class="form-control" id="name" v-model="address">
                     </div>
                    <div class="mb-3">
                        <label>Phone Number</label>
                          <input type="text" class="form-control" id="contact_number" v-model="contact_number">
                     </div>
                     <div class="mb-3">
                        <label>Website</label>
                          <input type="text" class="form-control" id="name" v-model="website">
                     </div>
                    <button type='submit' class="btn btn-info w-100">Register</button>
            </form>
            <div class="mt-3 text-center">
                <router-link to="/">Already have an account? Login</router-link>
            </div>
        </div>
    </div>
 </div>

</template>
