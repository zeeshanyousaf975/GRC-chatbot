FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json package-lock.json* ./
RUN npm ci

# Copy application code
COPY . .

# Build the application for production
RUN npm run build

# Expose port
EXPOSE 3000

# Start the application
CMD ["npm", "start"] 