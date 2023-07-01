
export const state = () => ({
  isAuthenticated: !!localStorage.getItem('token')
});

export const mutations = {
  SET_AUTHENTICATED(state, isAuthenticated) {
    state.isAuthenticated = isAuthenticated;
  },
};

export const actions = {
  async login({ commit }, { username, password }) {
    try {
      const response = await this.$axios.post(`/api/auth/login`, { username, password });
      localStorage.setItem('token', response.data.data.access);
      commit('SET_AUTHENTICATED', true);
    } catch (error) {
      throw error;
    }
  },
  logout({ commit }) {
    localStorage.removeItem('token');
    commit('SET_AUTHENTICATED', false);
  },
};

export const getters = {
  isAuthenticated(state) {
    return state.isAuthenticated;
  },
};
