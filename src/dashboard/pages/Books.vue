<template>
    <div>
      <h1 class="d-flex justify-content-center">Books</h1>
      <div class="d-flex justify-content-center">
        <div class="col-md-8">
          <div class="d-flex align-items-center justify-content-between mb-3">
            <div>
              <label for="searchInput">Search Books:</label>
              <b-input v-model="searchQuery" id="searchInput" size="lg" @input="searchBooks"></b-input>
            </div>
            <b-button @click="openAddBookModal" variant="primary">Add Book</b-button>
          </div>

          <b-table v-if="paginatedBooks.length > 0" striped hover :items="paginatedBooks" :fields="fields" @row-clicked="openEditBookModal">
            <template #cell(name)="row">
              {{ row.item.name }}
            </template>
            <template #cell(author)="row">
              {{ row.item.author.name }}
            </template>
            <template #cell(pages)="row">
              {{ row.item.pages }}
            </template>
          </b-table>
          <div v-else>
            <p>No books found.</p>
          </div>
            <!-- Pagination controls -->
        <b-pagination v-model="currentPage" :total-rows="filteredBooks.length" :per-page="perPage" align="center"></b-pagination>
        </div>
      </div>

      <!-- Add Book Modal -->
      <b-modal v-model="isAddBookModalOpen" title="Add Book" hide-footer>
        <b-form @submit.prevent="addBook">
          <b-form-group label="Name" label-for="bookName" :label-cols="4">
            <b-form-input v-model="newBook.name" id="bookName" required></b-form-input>
          </b-form-group>
          <b-form-group label="Number of Pages" label-for="bookPages" :label-cols="4">
            <b-form-input v-model="newBook.pages" id="bookPages" type="number" required></b-form-input>
          </b-form-group>
          <b-form-group label="Author" label-for="bookAuthor" :label-cols="4">
            <vue-treeselect v-model="newBook.author" :options="authorOptions" :multiple="false" :clearable="true" placeholder="Select an author"  :searchable="true" required />
          </b-form-group>

          <b-button type="submit" variant="success">Save</b-button>
        </b-form>
      </b-modal>

      <!-- Edit Book Modal -->
      <b-modal v-model="isEditBookModalOpen" title="Edit Book" hide-footer>
        <b-form @submit.prevent="saveBookChanges">
          <b-form-group label="Name" label-for="editBookName" :label-cols="4">
            <b-form-input v-model="editedBook.name" id="editBookName" required></b-form-input>
          </b-form-group>
          <b-form-group label="Number of Pages" label-for="editBookPages" :label-cols="4">
            <b-form-input v-model="editedBook.pages" id="editBookPages" type="number" required></b-form-input>
          </b-form-group>
          <b-form-group label="Author" label-for="editBookAuthor" :label-cols="4">
            <vue-treeselect v-model="editedBook.author.id" :options="authorOptions" :multiple="false" :clearable="true" :searchable="true" placeholder="Select an author" />
          </b-form-group>

          <b-button type="submit" variant="success">Save Changes</b-button>
        </b-form>
      </b-modal>
    </div>
  </template>

  <script>
  import VueTreeselect from '@riophae/vue-treeselect';
  import '@riophae/vue-treeselect/dist/vue-treeselect.css';
  import { chunk } from 'lodash';
  const authconfig = {
      headers: {
        Bearer: `${localStorage.getItem('token')}`
      }
    };


  export default {
    components: {
      VueTreeselect,
    },
    data() {
      return {
        searchQuery: '',
        isAddBookModalOpen: false,
        isEditBookModalOpen: false,
        newBook: {
          name: '',
          pages: null,
          author: null,
        },
        editedBook: {
          id: "",
          name: '',
          pages: '',
          author: {"id":null},
        },
        books: [],
        authors: [],
        fields: [{
            key: 'name'
          },
          {
            key: 'page_numbers',
            sortable: true,
          },
          {
            key: 'author'
          },
        ],
        currentPage: 1,
        perPage: 10,
      };
    },
    computed: {
      filteredBooks() {
        if (this.searchQuery) {
          return this.books.filter((book) =>
            book.name.toLowerCase().includes(this.searchQuery.toLowerCase())
          );
        } else {
          return this.books;
        }
      },
      paginatedBooks() {
        return chunk(this.filteredBooks, this.perPage)[this.currentPage - 1] || [];
    },
      authorOptions() {
        return this.authors.map((author) => ({
        id: author.id,
        label: author.name,
        author: author
    }));
  },
    },
    created() {
        this.fetchBooks();
        this.fetchAuthors()
    },
    methods: {
      searchBooks() {
        // Implement search logic here
      },
      openAddBookModal() {
        this.isAddBookModalOpen = true;
      },

      async addBook() {
        try {
            const response = await this.$axios.post(`/api/book`, {
                 "name":this.newBook.name,
                "pages":parseInt(this.newBook.pages),
                "author":this.newBook.author
            },authconfig);
            const newBook = response.data;
            this.books.push(newBook);
            this.isAddBookModalOpen = false;
            this.newBook = {
            name: '',
            pages: '',
            author: null,
        };
        } catch (error) {
            console.error('Error adding book:', error);
            this.isAddBookModalOpen = false;
        }
    },

      openEditBookModal(book) {
        this.editedBook = { ...book };
        this.editedBook.author = book.author;
        this.editedBook.pages = book.page_numbers;
        this.isEditBookModalOpen = true;
      },
      async saveBookChanges() {
        try {
            const response = await this.$axios.put(`/api/books/${this.editedBook.id}`, {
                "name":this.editedBook.name,
                "author_id": this.editedBook.author.id,
                "page_numbers":this.editedBook.pages
            },authconfig);
            this.fetchBooks();
            this.isEditBookModalOpen = false;
        } catch (error) {
            console.error('Error updating book:', error);
            this.isEditBookModalOpen = false;
        }
      },
      async fetchBooks() {
        try {
            const response = await this.$axios.get(`/api/books`,authconfig);
            this.books = response.data;
        } catch (error) {
            console.error('Error fetching books:', error);
        }
    },
    async fetchAuthors() {
        try {
            const response = await this.$axios.get(`/api/authors`,authconfig);
            this.authors = response.data;
        } catch (error) {
            console.error('Error fetching authors:', error);
        }
    }
    },


  };
  </script>
