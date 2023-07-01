<template>
    <div>
      <h1 class="d-flex justify-content-center">Authors</h1>
      <div class="d-flex justify-content-center">
      <div class="col-md-8">
        <div class="d-flex align-items-center justify-content-between mb-3">
          <div>
            <label for="searchInput">Search Authors:</label>
            <b-input v-model="searchQuery" id="searchInput" size="lg" @input="searchAuthors"></b-input>
          </div>
          <b-button @click="openAddAuthorModal" variant="primary">Add Author</b-button>
        </div>

        <b-table  v-if="paginatedAuthors.length > 0" striped hover :items="paginatedAuthors" :fields="fields" @row-clicked="openEditAuthorModal">
        </b-table>

        <div v-else>
          <p>No authors found.</p>
        </div>

        <b-pagination v-model="currentPage" :total-rows="filteredAuthors.length" :per-page="perPage" align="center"></b-pagination>

      </div>
    </div>


      <b-modal v-model="isAddAuthorModalOpen" title="Add Author" hide-footer>
        <b-form @submit.prevent="addAuthor" >
          <b-form-group label="Name" label-for="authorName" :label-cols="4">
            <b-form-input v-model="newAuthor.name" id="authorName" required></b-form-input>
          </b-form-group>

          <h3>Books:</h3>
          <b-table striped hover :items="newAuthor.books">
            <template #cell(name)="row">
              <b-form-input v-model="row.item.name"></b-form-input>
            </template>
            <template #cell(pages)="row">
              <b-form-input v-model="row.item.pages" type="number"></b-form-input>
            </template>
          </b-table>

          <b-button @click="addBook" variant="primary">Add Book</b-button>
          <b-button type="submit" variant="success">Save</b-button>
        </b-form>
      </b-modal>


      <b-modal v-model="isEditAuthorModalOpen" title="Edit Author" hide-footer>
        <b-form @submit.prevent="saveAuthorChanges">
          <b-form-group label="Name" label-for="editAuthorName" :label-cols="4">
            <b-form-input v-model="editedAuthor.name" id="editAuthorName" required></b-form-input>
          </b-form-group>

          <h3>Books:</h3>
          <b-table striped hover :items="editedAuthor.books" :fields="bfields">
            <template #cell(name)="row">
              <b-form-input v-model="row.item.name"></b-form-input>
            </template>
            <template #cell(page_numbers)="row">
              <b-form-input v-model="row.item.page_numbers" type="number"></b-form-input>
            </template>
            <template #cell(id)="row">
              <b-button @click="deleteEditedBook(row.index)" variant="danger">Delete</b-button>
            </template>
          </b-table>
          <b-button type="submit" variant="success">Save Changes</b-button>
        </b-form>
      </b-modal>
    </div>
  </template>



  <script>
  import { chunk } from 'lodash';
    const authconfig = {
      headers: {
        Bearer: `${localStorage.getItem('token')}`
      }
    };


  export default {
    data() {
      return {
        searchQuery: '',
        isAddAuthorModalOpen: false,
        isEditAuthorModalOpen: false,
        newAuthor: {
          name: '',
          books: [],
        },
        editedAuthor: {
          name: '',
          books: [],
        },
        authors: [],
        currentPage: 1,
        perPage: 10,
        fields: [{
            key: 'name'
          },
          {
            key: 'book_count',
            label: 'Number of Books',
            sortable: true,
          }],
          bfields: ['name','page_numbers', 'id'],
      };

    },
    computed: {
      filteredAuthors() {
        if (this.searchQuery) {
          return this.authors.filter((author) =>
            author.name.toLowerCase().includes(this.searchQuery.toLowerCase())
          );
        } else {
          return this.authors;
        }
      },
      paginatedAuthors() {

        return chunk(this.filteredAuthors, this.perPage)[this.currentPage - 1] || [];
    },
    },
    created() {
        this.fetchAuthors();
    },
    methods: {
      searchAuthors() {
      },
      openAddAuthorModal() {
        this.isAddAuthorModalOpen = true;
      },
      async addAuthor() {
        try {
            const response = await this.$axios.post(`/api/author`, this.newAuthor,authconfig);
            const newAuthor = response.data;
            this.authors.push(newAuthor);
            this.fetchAuthors();
            this.isAddAuthorModalOpen = false;
            this.newAuthor = {
                name: '',
                books: [],
            };
        } catch (error) {
            console.error('Error adding author:', error);
            this.isAddAuthorModalOpen = false;
        }
    },

      addBook() {
        this.newAuthor.books.push({ name: '', pages: 0 });
      },
      openEditAuthorModal(author) {
        this.editedAuthor = { ...author };
        this.isEditAuthorModalOpen = true;
      },
      async saveAuthorChanges() {
        try {
            const response = await this.$axios.put(`/api/authors/${this.editedAuthor.id}`, {
                "name":this.editedAuthor.name,
                "books": this.editedAuthor.books
            },authconfig);
            this.fetchAuthors();
            this.isEditAuthorModalOpen = false;
        } catch (error) {
            console.error('Error updating author:', error);
            this.isEditAuthorModalOpen = false
        }
      },
      deleteEditedBook(index) {
        this.editedAuthor.books.splice(index, 1);
      },
      async fetchAuthors() {
        try {
            const response = await this.$axios.get(`/api/authors`, authconfig);
            this.authors = response.data;
        } catch (error) {
            console.error('Error fetching authors:', error);
        }
    }
    },
  };
  </script>
