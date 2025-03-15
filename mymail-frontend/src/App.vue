<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center p-4">
    <h1 class="text-5xl font-extrabold mb-8 text-blue-800">Mymail</h1>

    <div class="bg-white shadow-lg rounded-lg p-8 w-full max-w-md transition-shadow duration-300 hover:shadow-2xl">
      <h2 class="text-xl font-semibold mb-3">Your Temporary Email</h2>
      <div class="flex items-center justify-between bg-gray-100 p-4 rounded-lg">
        <span class="text-gray-800">{{ tempEmail }}</span>
        <button @click="copyEmail" class="bg-blue-700 text-white px-5 py-3 rounded-lg transition-colors duration-200 hover:bg-blue-800 focus:outline-none focus:ring-2 focus:ring-blue-600">
          Copy
        </button>
      </div>
      <div v-if="isCopied" class="mt-2 text-green-600">Email copied!</div>
    </div>

    <div class="bg-white shadow-lg rounded-lg p-6 w-full max-w-md mt-6">
      <h2 class="text-xl font-semibold mb-3">Inbox</h2>
      <div v-if="isLoading" class="flex items-center justify-center text-gray-500 text-center">
  <svg class="animate-spin h-5 w-5 mr-3 text-blue-600" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24"><circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle><path class="opacity-75" fill="currentColor" d="M4 12c0-4.418 3.582-8 8-8s8 3.582 8 8-3.582 8-8 8-8-3.582-8-8z"></path></svg>
        <span>Loading emails...</span>
      </div>
      <div v-else-if="emails.length === 0" class="text-gray-500 text-center">
        <span>No new emails</span>
      </div>
      <ul v-else class="divide-y divide-gray-200">
        <li class="p-3 hover:bg-gray-100 cursor-pointer transition-colors duration-200 rounded-lg"
          v-for="email in emails"
          :key="email.id"
          class="p-3 hover:bg-gray-100 cursor-pointer transition-colors duration-200"
        >
          <div class="font-medium">{{ email.subject }}</div>
          <div class="text-sm text-gray-500">{{ email.sender }}</div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      tempEmail: "your-email@mymail.com",
      emails: [],
      isLoading: true,
      isCopied: false,
    };
  },
  methods: {
    async fetchEmails() {
      this.isLoading = true;
      try {
        const response = await axios.get("http://localhost:8000/emails");
        this.emails = response.data;
      } catch (error) {
        console.error("Error fetching emails:", error);
      } finally {
        this.isLoading = false;
      }
    },
    copyEmail() {
      navigator.clipboard.writeText(this.tempEmail);
      this.isCopied = true;
      setTimeout(() => {
        this.isCopied = false;
      }, 2000);
    },
  },
  mounted() {
    this.fetchEmails();
    setInterval(this.fetchEmails, 10000); // Refresh emails every 10s
  },
};
</script>

<style scoped>
/* Add extra styles if needed */
</style>
