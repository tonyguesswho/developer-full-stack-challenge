<template>
    <div>
      <div>
        <b-jumbotron>
          <template #lead>
            Welcome to the open source library
          </template>
          <hr class="my-4">
          <p>
            Take a look at the available authors and books by clicking below
          </p>
          <nuxt-link to="/authors" class="btn btn-primary">Authors</nuxt-link>
          <nuxt-link to="/books" class="btn btn-success">Books</nuxt-link>
        </b-jumbotron>
      </div>
    </div>
  </template>

  <script>
  export default {
    name: 'HomePage'
  }
  </script>
