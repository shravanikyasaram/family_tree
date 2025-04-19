import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const apiService = {
    addAncestor: async (data) => {
        try {
            const response = await axios.post(`${API_BASE_URL}/individuals`, data);
            return response.data;
        } catch (error) {
            console.error('Error adding ancestor:', error);
            throw error;
        }
    },
};

export default apiService;
