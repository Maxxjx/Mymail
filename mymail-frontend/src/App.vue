<template>
  <div class="min-h-screen bg-gray-50 flex flex-col items-center p-4">
    <h1 class="text-4xl font-bold mb-6 text-blue-700">Mymail</h1>

    <div class="bg-white shadow-lg rounded-lg p-6 w-full max-w-md transition-shadow duration-300 hover:shadow-xl">
      <h2 class="text-xl font-semibold mb-3">Your Temporary Email</h2>
      <div class="flex items-center justify-between bg-gray-100 p-4 rounded-lg">
        <span class="text-gray-800">{{ tempEmail }}</span>
        <button @click="copyEmail" class="bg-blue-600 text-white px-4 py-2 rounded transition-colors duration-200 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500">
          Copy
        </button>
      </div>
      <div v-if="isCopied" class="mt-2 text-green-600">Email copied!</div>
    </div>

    <div class="bg-white shadow-lg rounded-lg p-6 w-full max-w-md mt-6">
      <h2 class="text-xl font-semibold mb-3">Inbox</h2>
      <div v-if="isLoading" class="text-gray-500 text-center">
        <span>Loading emails...</span>
      </div>
      <div v-else-if="emails.length === 0" class="text-gray-500 text-center">
        <span>No new emails</span>
      </div>
      <ul v-else class="divide-y divide-gray-200">
        <li
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
