<template>
  <div class="add-graduate">
    <div class="header">

    </div>
    <div class="form-box">
      <h1>Agregar Egresado</h1>
      <form @submit.prevent="addGraduate">
        <div class="form-row">
          <div class="input-group">
            <label for="ag">AG</label>
            <input type="text" v-model="ag" required>
          </div>
          <div class="input-group">
            <label for="aa">AA</label>
            <input type="text" v-model="aa" required>
          </div>
        </div>
        <div class="form-row">
          <div class="input-group">
            <label for="pg">PG</label>
            <input type="text" v-model="pg" required>
          </div>
          <div class="input-group">
            <label for="pa">PA</label>
            <input type="text" v-model="pa" required>
          </div>
        </div>
        <div class="form-row">
          <div class="input-group">
            <label for="rendimiento">Rendimiento</label>
            <input type="text" v-model="rendimiento" required>
          </div>
          <div class="input-group">
            <label for="fecha_grado">Fecha de Grado</label>
            <input type="date" v-model="fecha_grado" required>
          </div>
        </div>
        <div class="form-row">
          <div class="input-group">
            <label for="cod_carrera">Código de Carrera</label>
            <input type="text" v-model="cod_carrera" required>
          </div>
          <div class="input-group">
            <label for="cod_periodo">Código de Periodo</label>
            <input type="text" v-model="cod_periodo" required>
          </div>
        </div>
        <div class="form-row">
          <div class="input-group">
            <label for="num_periodo">Número de Periodo</label>
            <input type="text" v-model="num_periodo" required>
          </div>
          <div class="input-group">
            <label for="cedula">Cédula</label>
            <input type="text" v-model="cedula" required>
          </div>
        </div>
        <div class="input-group">
          <label for="nombre">Nombre</label>
          <input type="text" v-model="nombre" required>
        </div>
        <button type="submit">Guardar</button>
      </form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AddGraduate',
  data() {
    return {
      ag: '',
      aa: '',
      pg: '',
      pa: '',
      rendimiento: '',
      fecha_grado: '',
      cod_carrera: '',
      cod_periodo: '',
      num_periodo: '',
      cedula: '',
      nombre: ''
    }
  },
  methods: {
    async addGraduate() {
      try {
        const token = localStorage.getItem('token');
        const response = await fetch('/api/agregar', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': token
          },
          body: JSON.stringify({
            ag: this.ag,
            aa: this.aa,
            pg: this.pg,
            pa: this.pa,
            rendimiento: this.rendimiento,
            fecha_grado: this.fecha_grado,
            cod_carrera: this.cod_carrera,
            cod_periodo: this.cod_periodo,
            num_periodo: this.num_periodo,
            cedula: this.cedula,
            nombre: this.nombre
          })
        });
        if (response.ok) {
          alert('Egresado agregado con éxito');
          this.resetForm();
        } else {
          const errorData = await response.json();
          alert(`Error al agregar egresado: ${errorData.error}`);
        }
      } catch (error) {
        console.error('Error:', error);
        alert('Error al agregar egresado');
      }
    },
    resetForm() {
      this.ag = '';
      this.aa = '';
      this.pg = '';
      this.pa = '';
      this.rendimiento = '';
      this.fecha_grado = '';
      this.cod_carrera = '';
      this.cod_periodo = '';
      this.num_periodo = '';
      this.cedula = '';
      this.nombre = '';
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

.add-graduate {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: calc(100vh - 70px); /* Altura ajustada para dejar espacio a la barra de tareas */
  padding-top: 70px; /* Añadir espacio arriba para la barra de tareas */
  color: #fff;
  position: relative;
}

.header {
  position: absolute;
  top: 20px;
  width: 100%;
  display: flex;
  justify-content: center;
}

.form-box {
  background: rgba(0, 0, 102, 0.8); /* Fondo semitransparente azul oscuro */
  color: #fff;
  padding: 40px 60px;
  border-radius: 10px;
  text-align: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  width: 60%;
}

h1 {
  font-size: 3em; /* Texto más grande */
  margin-bottom: 20px;
}

.form-row {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
}

.input-group {
  width: 48%; /* Ajustar ancho para dividir en dos columnas */
  text-align: left;
}

label {
  font-size: 1.2em;
  margin-bottom: 5px;
  display: block;
}

input[type="text"],
input[type="date"] {
  width: 100%;
  padding: 10px;
  font-size: 1em;
  border: none;
  border-radius: 5px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  margin-top: 5px;
}

button {
  padding: 15px 30px;
  font-size: 18px;
  cursor: pointer;
  color: #000066;
  background: #fff;
  border: none;
  border-radius: 5px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.3);
  transition: background-color 0.3s, transform 0.3s;
  margin-top: 20px;
}

button:hover {
  background-color: #e0e0e0;
  transform: translateY(-4px);
}
</style>
