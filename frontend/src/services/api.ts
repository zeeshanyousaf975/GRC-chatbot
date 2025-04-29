import axios from 'axios';

// API base URL
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  // Longer timeout for LLM responses
  timeout: 60000, // 60 seconds
});

// Local storage key for session ID
const SESSION_ID_KEY = 'chat_session_id';

// Response interface
interface ChatResponse {
  response: string;
  success: boolean;
  error: string;
  session_id?: string;
}

/**
 * Get the current session ID from local storage
 * @returns The session ID or undefined if not found
 */
export const getSessionId = (): string | null => {
  const sessionId = localStorage.getItem(SESSION_ID_KEY);
  console.log(`[DEBUG] Getting session ID from storage: ${sessionId}`);
  return sessionId;
};

/**
 * Save the session ID to local storage
 * @param sessionId The session ID to save
 */
export const saveSessionId = (sessionId: string): void => {
  console.log(`[DEBUG] Saving session ID to storage: ${sessionId}`);
  localStorage.setItem(SESSION_ID_KEY, sessionId);
};

/**
 * Clear the session ID from local storage
 */
export const clearSessionId = (): void => {
  console.log(`[DEBUG] Clearing session ID from storage`);
  localStorage.removeItem(SESSION_ID_KEY);
};

/**
 * Send a message to the chat API
 * @param message The message to send
 * @returns The response text from the assistant
 */
export const sendMessage = async (message: string): Promise<string> => {
  try {
    console.log(`[DEBUG] Sending message to API: ${message}`);
    
    // Get session ID from local storage
    const sessionId = getSessionId();
    console.log(`[DEBUG] Using session ID: ${sessionId || 'none'}`);
    
    // Include session ID in request if available
    const requestData: Record<string, any> = { message };
    if (sessionId) {
      requestData.session_id = sessionId;
      
      // Also include in headers for redundancy
      api.defaults.headers.common['X-Session-ID'] = sessionId;
      console.log(`[DEBUG] Added session ID to headers and request body`);
    }
    
    console.log(`[DEBUG] Request data:`, requestData);
    const response = await api.post<ChatResponse>('/chat', requestData);
    console.log(`[DEBUG] Received response:`, response.data);
    
    // Check if the response indicates an error
    if (!response.data.success) {
      console.error(`API Error: ${response.data.error}`);
      throw new Error(response.data.error || 'Failed to send message');
    }
    
    // Save the session ID if provided in the response
    if (response.data.session_id) {
      saveSessionId(response.data.session_id);
      console.log(`[DEBUG] Saved session ID from response: ${response.data.session_id}`);
    } else {
      console.warn(`[DEBUG] No session ID returned in response`);
    }
    
    return response.data.response;
  } catch (error) {
    console.error('[DEBUG] API Error:', error);
    
    // If we have a response from the server with an error message, use it
    if (axios.isAxiosError(error) && error.response?.data?.response) {
      // Save session ID even if there was an error
      if (error.response.data.session_id) {
        saveSessionId(error.response.data.session_id);
        console.log(`[DEBUG] Saved session ID from error response: ${error.response.data.session_id}`);
      }
      return error.response.data.response;
    }
    
    // Otherwise, throw a generic error
    throw new Error('Failed to communicate with the chat service. Please try again.');
  }
};

/**
 * Clear the chat history
 * @returns Success status
 */
export const clearChatHistory = async (): Promise<boolean> => {
  try {
    const sessionId = getSessionId();
    console.log(`[DEBUG] Clearing chat history for session: ${sessionId || 'none'}`);
    const response = await api.post('/chat/clear', { session_id: sessionId });
    console.log(`[DEBUG] Clear history response:`, response.data);
    return response.data.success || false;
  } catch (error) {
    console.error('[DEBUG] Error clearing chat history:', error);
    return false;
  }
}; 