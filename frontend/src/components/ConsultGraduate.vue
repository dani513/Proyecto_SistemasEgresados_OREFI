<template>
  <SelectSearchType />
</template>

<script>
import SelectSearchType from './SelectSearchType.vue'

export default {
  name: 'ConsultGraduate',
  components: {
    SelectSearchType
  }
}
</script>

<style scoped>
.consult-graduate {
  text-align: center;
  margin-top: 50px;
}
form div {
  margin-bottom: 10px;
}
button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
}
</style>
