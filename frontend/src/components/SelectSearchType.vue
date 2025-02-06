<template>
  <div class="select-search-type">
    <h1>Consultar Egresado</h1>
    <div class="buttons">
      <button @click="setSearchType('codigo_carrera')" :class="{ active: searchType === 'codigo_carrera' }">Código de Carrera</button>
      <button @click="setSearchType('cedula')" :class="{ active: searchType === 'cedula' }">Cédula</button>
      <button @click="setSearchType('nombre')" :class="{ active: searchType === 'nombre' }">Nombre</button>
      <button @click="setSearchType('codigo_periodo')" :class="{ active: searchType === 'codigo_periodo' }">Código de Período</button>
    </div>
    <div v-if="searchType" class="search-box">
      <label v-if="searchType === 'codigo_carrera'" for="codigo_carrera">Código de Carrera</label>
      <input v-if="searchType === 'codigo_carrera'" type="text" v-model="codigo_carrera" @keyup.enter="consultGraduate">

      <label v-if="searchType === 'cedula'" for="cedula">Cédula</label>
      <input v-if="searchType === 'cedula'" type="text" v-model="cedula" @keyup.enter="consultGraduate">

      <label v-if="searchType === 'nombre'" for="nombre">Nombre</label>
      <input v-if="searchType === 'nombre'" type="text" v-model="nombre" @keyup.enter="consultGraduate">

      <label v-if="searchType === 'codigo_periodo'" for="codigo_periodo">Código de Período</label>
      <input v-if="searchType === 'codigo_periodo'" type="text" v-model="codigo_periodo" @keyup.enter="consultGraduate">

      <button @click="consultGraduate">Consultar</button>
    </div>
    <div v-if="egresados.length" class="results-box">
      <h2>Resultados de la Consulta</h2>
      <ul>
        <li v-for="egresado in egresados" :key="egresado.id" @click="selectEgresado(egresado)">
          {{ egresado.nombre }} - {{ egresado.cedula }} - {{ egresado.cod_carrera }}
        </li>
      </ul>
    </div>
    <div v-if="selectedEgresado" class="details-box">
      <h2>Detalles del Egresado</h2>
      <p><strong>AG:</strong> {{ selectedEgresado.ag }}</p>
      <p><strong>AA:</strong> {{ selectedEgresado.aa }}</p>
      <p><strong>PG:</strong> {{ selectedEgresado.pg }}</p>
      <p><strong>PA:</strong> {{ selectedEgresado.pa }}</p>
      <p><strong>Nombre:</strong> {{ selectedEgresado.nombre }}</p>
      <p><strong>Cédula:</strong> {{ selectedEgresado.cedula }}</p>
      <p><strong>Código de Carrera:</strong> {{ selectedEgresado.cod_carrera }}</p>
      <p><strong>Código de Período:</strong> {{ selectedEgresado.cod_periodo }}</p>
      <p><strong>Fecha de Grado:</strong> {{ selectedEgresado.fecha_grado }}</p>

      <button @click="deleteEgresado(selectedEgresado.id)">Borrar</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'SelectSearchType',
  data() {
    return {
      searchType: '',
      codigo_carrera: '',
      cedula: '',
      nombre: '',
      codigo_periodo: '',
      egresados: [],
      selectedEgresado: null
    }
  },
  methods: {
    setSearchType(type) {
      this.searchType = type;
      this.codigo_carrera = '';
      this.cedula = '';
      this.nombre = '';
      this.codigo_periodo = '';
      this.egresados = [];
      this.selectedEgresado = null;
    },
    async consultGraduate() {
      const token = localStorage.getItem('token');
      let queryParams = '';
      if (this.searchType === 'codigo_carrera') {
        queryParams = `codigo_carrera=${this.codigo_carrera}`;
      } else if (this.searchType === 'cedula') {
        queryParams = `cedula=${this.cedula}`;
      } else if (this.searchType === 'nombre') {
        queryParams = `nombre=${this.nombre}`;
      } else if (this.searchType === 'codigo_periodo') {
        queryParams = `codigo_periodo=${this.codigo_periodo}`;
      }

      const response = await fetch(`/api/consultar?${queryParams}`, {
        method: 'GET',
        headers: {
          'Authorization': token
        }
      });
      if (response.ok) {
        this.egresados = await response.json();
      } else {
        alert('Error al consultar egresados');
      }
    },
    selectEgresado(egresado) {
      this.selectedEgresado = egresado;
    },
    async deleteEgresado(id) {
      const token = localStorage.getItem('token');
      const response = await fetch(`/api/eliminar/${id}`, {
        method: 'POST',
        headers: {
          'Authorization': token
        }
      });
      if (response.ok) {
        alert('Egresado eliminado con éxito');
        this.selectedEgresado = null;
        this.consultGraduate();
      } else {
        alert('Error al eliminar egresado');
      }
    }
  }
}
</script>

<style scoped>
body, html {
  margin: 0;
  padding: 0;
  height: 100%;
  background: url('@/assets/background.jpg') no-repeat center center fixed; /* Imagen de fondo */
  background-size: cover; /* Asegura que la imagen cubra toda la pantalla */
}

.select-search-type {
  text-align: center;
  padding: 70px 20px; /* Añadir espacio superior para la barra de tareas */
  color: #fff;
}

h1 {
  font-size: 3em;
  margin-bottom: 20px;
  color: black;
}

.buttons {
  margin-bottom: 20px;
}

button {
  padding: 10px 20px;
  font-size: 16px;
  cursor: pointer;
  margin: 5px;
  color: #fff;
  background-color: #000066;
  border: none;
  border-radius: 5px;
  transition: background-color 0.3s, transform 0.3s;
}

button:hover {
  background-color: #333399;
  transform: translateY(-4px);
}

button.active {
  background-color: #333399;
}

.search-box,
.results-box,
.details-box {
  background: rgba(0, 0, 102, 0.8); /* Fondo semitransparente azul oscuro */
  padding: 20px;
  border-radius: 10px;
  text-align: left;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  margin-bottom: 20px;
  width: 80%; /* Ajustar ancho */
  max-width: 600px; /* Ancho máximo */
  margin-left: auto; /* Centrando */
  margin-right: auto; /* Centrando */
}

label {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  color: #fff;
}

input {
  display: block;
  width: 100%;
  margin-bottom: 10px;
  color: black;
}

input {
  padding: 10px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

ul {
  list-style-type: none;
  padding: 0;
}

li {
  cursor: pointer;
  padding: 10px;
  background: rgba(255, 255, 255, 0.1);
  margin-bottom: 5px;
  border-radius: 5px;
  transition: background-color 0.3s;
}

li:hover {
  background-color: rgba(255, 255, 255, 0.2);
}

p {
  font-size: 1.1em;
  margin-bottom: 10px;
}
</style>
