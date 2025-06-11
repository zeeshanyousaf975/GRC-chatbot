import axios, { AxiosInstance } from 'axios';

// Define API response types
export interface QueryResponse {
  response: string;
  sourceDocuments?: any[];
}

export interface NavigateResponse {
  directions: string;
  path?: any[];
  estimatedTime?: string;
}

export interface FeedbackResponse {
  success: boolean;
  message: string;
}

class ApiService {
  private client: AxiosInstance;
  private baseURL: string;

  constructor() {
    // Get API URL from environment variables with fallback
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
    
    console.log("API URL:", this.baseURL); // Add debug log
    
    // Create axios instance
    this.client = axios.create({
      baseURL: this.baseURL,
      headers: {
        'Content-Type': 'application/json',
      },
      timeout: 30000, // 30 second timeout
    });
    
    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        // Log the error
        console.error('API request failed:', error);
        
        // Create a meaningful error message
        let errorMessage = 'An unexpected error occurred. Please try again.';
        
        if (error.response) {
          // The request was made and the server responded with a status code
          // that falls out of the range of 2xx
          const status = error.response.status;
          const data = error.response.data;
          
          if (status === 404) {
            errorMessage = 'The requested resource was not found.';
          } else if (status === 401 || status === 403) {
            errorMessage = 'You are not authorized to access this resource.';
          } else if (status === 429) {
            errorMessage = 'Too many requests. Please try again later.';
          } else if (status >= 500) {
            errorMessage = 'The server encountered an error. Please try again later.';
          }
          
          // Use error message from API if available
          if (data && data.detail) {
            errorMessage = data.detail;
          }
        } else if (error.request) {
          // The request was made but no response was received
          errorMessage = 'No response received from server. Please check your internet connection.';
        }
        
        // Return a rejected promise with the error message
        return Promise.reject(new Error(errorMessage));
      }
    );
  }

  /**
   * Send a query to the chatbot
   */
  async sendQuery(question: string, chatHistory: any[] = []): Promise<QueryResponse> {
    try {
      console.log('Sending query to backend:', question); // Add debug log
      
      const response = await this.client.post('/api/query', {
        query: question, // Changed from 'question' to 'query' to match backend expectation
        chat_history: chatHistory
      });
      
      console.log('Response from backend:', response.data); // Add debug log
      return response.data;
    } catch (error) {
      // Throw the error to be handled by the component
      console.error('Error in sendQuery:', error); // Add debug log
      throw error;
    }
  }

  /**
   * Get navigation directions
   */
  async getNavigation(start: string, destination: string, preferences?: any): Promise<NavigateResponse> {
    try {
      const response = await this.client.post('/api/navigate', {
        start,
        destination,
        preferences: preferences || {}
      });
      
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Send user feedback about a response
   */
  async sendFeedback(responseId: string, rating: number, comments?: string): Promise<FeedbackResponse> {
    try {
      const response = await this.client.post('/api/feedback', {
        response_id: responseId,
        rating,
        comments: comments || ''
      });
      
      return response.data;
    } catch (error) {
      throw error;
    }
  }

  /**
   * Check API health
   */
  async checkHealth(): Promise<boolean> {
    try {
      console.log('Checking API health at:', this.baseURL); // Add debug log
      const response = await this.client.get('/');
      console.log('Health check response:', response.status); // Add debug log
      return response.status === 200;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  }
}

// Create and export a singleton instance
const apiService = new ApiService();
export default apiService; 