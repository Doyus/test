<template>
  <div>
    <footer class="footer" v-once>
      Copyright &copy; {{ getYear }} 国信创新 All Rights Reserved.
    </footer>
  </div>
</template>
<script>
export default {
  computed: {
    getYear() {
      return new Date().getFullYear();
    },
  },
};
</script>
