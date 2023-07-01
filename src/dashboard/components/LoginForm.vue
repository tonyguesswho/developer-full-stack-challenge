<template>
    <div>
    <b-alert v-if="errorMsg" variant="danger" show dismissible>
      {{ errorMsg }}
    </b-alert>
    <div class="card mt-5">
      <div class="card-header">Login</div>
      <div class="card-body">
        <form @submit.prevent="submitLogin">
          <div class="form-group">
            <label for="username">Username</label>
            <input type="text" class="form-control" id="username" v-model="username" required>
          </div>
          <div class="form-group">
            <label for="password">Password</label>
            <input type="password" class="form-control" id="password" v-model="password" required>
          </div>
          <button type="submit" class="btn btn-primary">Login</button>
        </form>
      </div>
    </div>
</div>
  </template>

  <script>
  export default {
    data() {
      return {
        username: '',
        password: ''
      };
    },
    props: {
    errorMsg: {
        required: true
    }
  },
    methods: {
      async submitLogin() {
        await this.$emit('login', {
            username: this.username,
            password: this.password,
        });

      },
    },
  };
  </script>

  <style scoped>
  .card {
    width: 400px;
    margin: 0 auto; /* Center the card horizontally */
  }
  </style>
