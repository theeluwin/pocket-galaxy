<template>
  <v-card class="mb-5 px-3 pb-3">

    <!-- header -->
    <v-row>
      <v-col sm="12">
        <h4>{{ document.title }}</h4>
      </v-col>
    </v-row>

    <!-- body -->
    <v-row>
      <v-col cols="12">
        <p>{{ document.content }}</p>
      </v-col>
    </v-row>

  </v-card>
</template>

<script>
  export default {
    name: 'Document',
    props: {
      document: Object
    },
  }
</script>
