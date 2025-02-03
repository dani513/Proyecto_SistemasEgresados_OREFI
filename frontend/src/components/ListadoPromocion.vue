<template>
  <div class="listado-promocion">
    <h2>Listado Promoción</h2>
    <div>
      <label for="codigo_carrera">Código de Carrera:</label>
      <select v-model="codigoCarrera" required>
        <option v-for="carrera in carreras" :key="carrera.cod_carrera" :value="carrera.cod_carrera">
          {{ carrera.nombre }}
        </option>
      </select>
    </div>
    <div>
      <label for="ano">Año de Período:</label>
      <select v-model="anoSeleccionado" @change="cargarPeriodos" required>
        <option v-for="ano in anos" :key="ano" :value="ano">
          {{ ano }}
        </option>
      </select>
    </div>
    <div>
      <label for="periodo">Período:</label>
      <select v-model="periodoSeleccionado" required>
        <option value="A">A</option>
        <option value="B">B</option>
        <option value="U">U</option>
        <option value="E">E</option>
        <option value="I">I</option>
      </select>
    </div>
    <div>
      <label for="tipo_lista">Tipo de Lista:</label>
      <select v-model="tipoLista" required>
        <option value="tipo1">Cuadro de Promoción por el Promedio Ponderado</option>
        <option value="tipo2">Cuadro de Promoción por el Promedio Aritmético</option>
        <option value="tipo3">Cuadro de Promoción en Orden Alfabético</option>
      </select>
    </div>
    <button @click="buscarEgresados">Buscar</button>
    
    <div v-if="egresados.length > 0">
      <h3>Resultados:</h3>
      <ul>
        <li v-for="egresado in egresados" :key="egresado.cedula">
          {{ egresado.nombre }} - {{ egresado.cedula }} - {{ egresado.rendimiento }}
        </li>
      </ul>
      <button @click="generarPDF">Generar PDF</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ListadoPromocion',
  data() {
    return {
      codigoCarrera: '',
      anoSeleccionado: '',
      periodoSeleccionado: '',
      tipoLista: 'tipo1',  // Por defecto, seleccionamos tipo 1
      anos: [],
      carreras: [],
      egresados: []
    };
  },
  created() {
    this.cargarCarreras();
    this.cargarAnos();
  },
  methods: {
    async cargarCarreras() {
      try {
        const response = await fetch('/api/carreras');
        if (response.ok) {
          this.carreras = await response.json();
        } else {
          console.error('Error al cargar las carreras');
        }
      } catch (error) {
        console.error('Error al cargar las carreras:', error);
      }
    },
    async cargarAnos() {
      try {
        const response = await fetch('/api/periodos');
        if (response.ok) {
          const periodos = await response.json();
          this.anos = [...new Set(periodos.map(periodo => periodo.ano))];
        } else {
          console.error('Error al cargar los años');
        }
      } catch (error) {
        console.error('Error al cargar los años:', error);
      }
    },
    async buscarEgresados() {
      const codigoPeriodo = `${this.periodoSeleccionado}${this.anoSeleccionado}`;
      try {
        const response = await fetch(`/api/listado-promocion?codigo_carrera=${this.codigoCarrera}&codigo_periodo=${codigoPeriodo}`);
        if (response.ok) {
          const data = await response.json();
          if (data.error) {
            alert(data.error);
            this.egresados = [];
          } else {
            this.egresados = data;
          }
        } else {
          alert('No se encontraron egresados o hubo un error en la búsqueda');
          this.egresados = [];
        }
      } catch (error) {
        console.error('Error al buscar egresados:', error);
        alert('Hubo un error en la búsqueda');
      }
    },
    generarPDF() {
      const codigoPeriodo = `${this.periodoSeleccionado}${this.anoSeleccionado}`;
      const url = `/api/generar-listado-promocion?codigo_carrera=${this.codigoCarrera}&codigo_periodo=${codigoPeriodo}&tipo_lista=${this.tipoLista}`;
      window.open(url, '_blank');
    }
  }
};
</script>

<style scoped>
  /* Estilos para el formulario */
.listado-promocion {
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin: 20px;
}

.listado-promocion h2 {
  font-size: 24px;
  margin-bottom: 20px;
}
.listado-promocion div {
  margin-bottom: 10px;
}

.listado-promocion label {
  display: block;
  font-weight: bold;
}

.listado-promocion input, .listado-promocion select {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.listado-promocion button {
  padding: 10px 15px;
  background-color: #336699;
  color: #fff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.listado-promocion button:hover {
  background-color: #5a9bd3;
}

.listado-promocion ul {
  list-style-type: none;
  padding: 0;
  margin-top: 20px;
}

.listado-promocion ul li {
  padding: 10px;
  background-color: #f9f9f9;
  border-bottom: 1px solid #ccc;
}

.listado-promocion ul li:last-child {
  border-bottom: none;
}
</style>
