<template>
    <div class="listado-promocion">
      <h2>Listado Promoción</h2>
      <div>
        <label for="codigo_carrera">Código de Carrera:</label>
        <input type="text" v-model="codigoCarrera" />
      </div>
      <div>
        <label for="codigo_periodo">Código de Período:</label>
        <input type="text" v-model="codigoPeriodo" />
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
        codigoPeriodo: '',
        egresados: []
      };
    },
    methods: {
      async buscarEgresados() {
        try {
          const response = await fetch(`/api/listado-promocion?codigo_carrera=${this.codigoCarrera}&codigo_periodo=${this.codigoPeriodo}`);
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
        const url = `/api/generar-listado-promocion?codigo_carrera=${this.codigoCarrera}&codigo_periodo=${this.codigoPeriodo}`;
        window.open(url, '_blank');
      }
    }
  };
  </script>
  
<style scoped> 
  /* Estilos para el formulario */ 
.listado-promocion { background-color: #fff; 
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

.listado-promocion input { 
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