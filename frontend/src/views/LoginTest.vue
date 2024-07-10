<!-- LoginTest.vue -->
<!-- Page should show what user we are logged in as and include a field to login -->
<!-- 

Endpoints:
- GET /auth/login -> {"authenticated": false}
- POST /auth/login ? {"username": "admin", "password": "admin"} -> {"authenticated": true}
- GET /auth/user -> {"username": "admin"}
- POST /auth/logout -> {"message": "logged out successfully"} (cannot error, always logged out)

 -->
<template>
  <div class="container mx-auto">
    <h1 class="text-4xl font-bold text-center mt-8">Login Test</h1>
    <p class="text-lg text-center mt-4">This is the Login Test view</p>
    <div class="flex justify-center mt-8">
      <button class="bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded" @click="login">
        Login
      </button>
    </div>
    <div class="flex justify-center mt-8">
      <button class="bg-red-500 hover:bg-red-700 text-white font-bold py-2 px-4 rounded" @click="logout">
        Logout
      </button>
    </div>
    <div class="flex justify-center mt-8">
      <p v-if="authenticated">Logged in as {{ username }}</p>
      <p v-else>Not logged in</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      authenticated: false,
      username: null
    }
  },
  mounted() {
    this.getUsername();
  },
  methods: {
    getCsrfToken() {
      return document.querySelector('meta[name="csrf-token"]').getAttribute('content')
    },
    async login() {
      const csrfToken = this.getCsrfToken()
      const response = await fetch('/auth/login/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
          username: 'test_user',
          password: 'password'
        })
      })
      const data = await response.json()
      if (data.authenticated) {
        this.authenticated = true

        location.reload()
      }
    },
    async getUsername() {
      const login_response = await fetch('/auth/login/', {
        headers: {
          'X-CSRFToken': this.getCsrfToken()
        }
      })

      const login_data = await login_response.json()
      this.authenticated = login_data.authenticated

      if (!this.authenticated) {
        return
      }

      const response = await fetch('/auth/user/', {
        headers: {
          'X-CSRFToken': this.getCsrfToken()
        }
      })
      const data = await response.json()
      this.username = data.username
    },
    async logout() {
      const csrfToken = this.getCsrfToken()
      await fetch('/auth/logout/', {
        method: 'POST',
        headers: {
          'X-CSRFToken': csrfToken
        }
      })
      this.authenticated = false
      this.username = null

      location.reload()
    }
  }
}
</script>


<style>
.container {
  max-width: 800px;
}
</style>