/**
 * Development setup script for frontend
 */
const fs = require('fs');
const path = require('path');

// Create .env file if it doesn't exist
const envFile = path.join(__dirname, '.env');
if (!fs.existsSync(envFile)) {
    console.log('Creating .env file for development...');
    const envContent = `# API URL for development
REACT_APP_API_URL=http://localhost:8000/api
# Set to true for more verbose console logs
REACT_APP_DEBUG=true
`;
    fs.writeFileSync(envFile, envContent);
    console.log('.env file created successfully.');
} else {
    console.log('.env file already exists, skipping creation.');
}

// Check for type dependencies
const packageJson = require('./package.json');
const missingTypes = [];

// Check for React types
if (!packageJson.dependencies['@types/react'] && !packageJson.devDependencies?.['@types/react']) {
    missingTypes.push('@types/react');
}

// Check for other types
['@types/react-dom', '@types/node', 'axios'].forEach(pkg => {
    if (!packageJson.dependencies[pkg] && !packageJson.devDependencies?.[pkg]) {
        missingTypes.push(pkg);
    }
});

if (missingTypes.length > 0) {
    console.log('\nSome type dependencies might be missing. Run the following command:');
    console.log(`npm install --save-dev ${missingTypes.join(' ')}`);
}

console.log('\nSetup complete! To start the development server:');
console.log('1. Run "npm install" to install dependencies');
console.log('2. Run "npm start" to start the development server'); 