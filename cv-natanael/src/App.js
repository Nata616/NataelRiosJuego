import React, { useRef } from 'react';
import html2canvas from 'html2canvas';
import jsPDF from 'jspdf';

function App() {
  const cvRef = useRef();

  const handleDownloadPDF = async () => {
    const element = cvRef.current;
    const canvas = await html2canvas(element, {
      scale: 2,
      useCORS: true,
      logging: false,
    });
    
    const imgData = canvas.toDataURL('image/png');
    const pdf = new jsPDF('p', 'mm', 'a4');
    const pdfWidth = pdf.internal.pageSize.getWidth();
    const pdfHeight = pdf.internal.pageSize.getHeight();
    const imgWidth = canvas.width;
    const imgHeight = canvas.height;
    const ratio = Math.min(pdfWidth / imgWidth, pdfHeight / imgHeight);
    const imgX = (pdfWidth - imgWidth * ratio) / 2;
    const imgY = 0;
    
    pdf.addImage(imgData, 'PNG', imgX, imgY, imgWidth * ratio, imgHeight * ratio);
    pdf.save('CV_Natanael_Rios.pdf');
  };

  const SkillBar = ({ skill, level }) => (
    <div className="mb-4">
      <div className="flex justify-between mb-1">
        <span className="text-sm font-medium text-gray-700">{skill}</span>
        <span className="text-sm font-medium text-gray-500">{level}%</span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2.5">
        <div 
          className="bg-gradient-to-r from-blue-500 to-blue-600 h-2.5 rounded-full transition-all duration-500"
          style={{ width: `${level}%` }}
        ></div>
      </div>
    </div>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 py-8 px-4">
      <div className="max-w-5xl mx-auto">
        {/* Botón de descarga */}
        <div className="flex justify-end mb-6">
          <button
            onClick={handleDownloadPDF}
            className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-3 rounded-lg shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-300 font-semibold flex items-center gap-2"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
            </svg>
            Descargar PDF
          </button>
        </div>

        {/* CV Container */}
        <div ref={cvRef} className="bg-white rounded-2xl shadow-2xl overflow-hidden">
          {/* Header */}
          <div className="bg-gradient-to-r from-blue-600 via-blue-700 to-blue-800 text-white p-8 md:p-12">
            <div className="flex flex-col md:flex-row items-center md:items-start gap-6">
              <div className="w-32 h-32 bg-white rounded-full flex items-center justify-center shadow-xl">
                <span className="text-5xl font-bold text-blue-600">NR</span>
              </div>
              <div className="flex-1 text-center md:text-left">
                <h1 className="text-4xl md:text-5xl font-bold mb-2">Natanael Rios</h1>
                <p className="text-xl md:text-2xl text-blue-100 mb-4">Desarrollador de Software en Formación</p>
                <div className="flex flex-wrap justify-center md:justify-start gap-4 text-sm">
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path d="M2.003 5.884L10 9.882l7.997-3.998A2 2 0 0016 4H4a2 2 0 00-1.997 1.884z" />
                      <path d="M18 8.118l-8 4-8-4V14a2 2 0 002 2h12a2 2 0 002-2V8.118z" />
                    </svg>
                    <span>natanael.rios@email.com</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
                    </svg>
                    <span>24 años</span>
                  </div>
                  <div className="flex items-center gap-2">
                    <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                    </svg>
                    <span>Avellaneda, Buenos Aires</span>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Content */}
          <div className="p-8 md:p-12">
            {/* Perfil Profesional */}
            <section className="mb-10">
              <h2 className="text-3xl font-bold text-gray-800 mb-4 pb-2 border-b-4 border-blue-600 inline-block">
                Perfil Profesional
              </h2>
              <p className="text-gray-700 leading-relaxed mt-4 text-lg">
                Estudiante de Tecnicatura en Programación con sólidos conocimientos en desarrollo de software 
                y bases de datos. Apasionado por la tecnología y el aprendizaje continuo, con habilidades en 
                múltiples lenguajes de programación y herramientas de desarrollo. Busco oportunidades para 
                aplicar mis conocimientos técnicos, contribuir a proyectos innovadores y crecer profesionalmente 
                en el campo del desarrollo de software.
              </p>
            </section>

            {/* Grid de 2 columnas */}
            <div className="grid md:grid-cols-2 gap-8">
              {/* Columna Izquierda */}
              <div>
                {/* Educación */}
                <section className="mb-10">
                  <h2 className="text-3xl font-bold text-gray-800 mb-6 pb-2 border-b-4 border-blue-600 inline-block">
                    Educación
                  </h2>
                  
                  <div className="mt-6 space-y-6">
                    {/* Educación Actual */}
                    <div className="relative pl-8 border-l-4 border-blue-600">
                      <div className="absolute -left-2.5 top-0 w-5 h-5 rounded-full bg-blue-600 border-4 border-white"></div>
                      <div className="bg-blue-50 p-4 rounded-lg">
                        <div className="flex items-start justify-between mb-2">
                          <h3 className="text-xl font-bold text-gray-800">Tecnicatura en Programación</h3>
                          <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full font-semibold">
                            En Curso
                          </span>
                        </div>
                        <p className="text-blue-700 font-semibold mb-1">Universidad Tecnológica Nacional (UTN)</p>
                        <p className="text-gray-600 text-sm mb-2">Sede Avellaneda - Sucursal Anto Pane</p>
                        <p className="text-gray-700 font-medium">2do Año • 2023 - Presente</p>
                      </div>
                    </div>

                    {/* Educación Completada */}
                    <div className="relative pl-8 border-l-4 border-gray-300">
                      <div className="absolute -left-2.5 top-0 w-5 h-5 rounded-full bg-gray-400 border-4 border-white"></div>
                      <div className="bg-gray-50 p-4 rounded-lg">
                        <h3 className="text-xl font-bold text-gray-800 mb-2">Bachillerato en Economía</h3>
                        <p className="text-gray-700 font-semibold mb-1">Instituto Cristo Rey</p>
                        <p className="text-gray-600">Título Completo</p>
                      </div>
                    </div>
                  </div>
                </section>

                {/* Herramientas y Tecnologías */}
                <section className="mb-10">
                  <h2 className="text-3xl font-bold text-gray-800 mb-6 pb-2 border-b-4 border-blue-600 inline-block">
                    Herramientas
                  </h2>
                  
                  <div className="mt-6 grid grid-cols-2 gap-4">
                    <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-4 rounded-lg text-center shadow-md hover:shadow-lg transition-shadow">
                      <div className="text-3xl mb-2">💻</div>
                      <h4 className="font-bold text-gray-800">IntelliJ IDEA</h4>
                      <p className="text-sm text-gray-600">IDE Principal</p>
                    </div>
                    <div className="bg-gradient-to-br from-purple-50 to-purple-100 p-4 rounded-lg text-center shadow-md hover:shadow-lg transition-shadow">
                      <div className="text-3xl mb-2">📝</div>
                      <h4 className="font-bold text-gray-800">VS Code</h4>
                      <p className="text-sm text-gray-600">Editor de Código</p>
                    </div>
                    <div className="bg-gradient-to-br from-red-50 to-red-100 p-4 rounded-lg text-center shadow-md hover:shadow-lg transition-shadow">
                      <div className="text-3xl mb-2">☕</div>
                      <h4 className="font-bold text-gray-800">NetBeans</h4>
                      <p className="text-sm text-gray-600">IDE Java</p>
                    </div>
                    <div className="bg-gradient-to-br from-green-50 to-green-100 p-4 rounded-lg text-center shadow-md hover:shadow-lg transition-shadow">
                      <div className="text-3xl mb-2">🤖</div>
                      <h4 className="font-bold text-gray-800">IA Tools</h4>
                      <p className="text-sm text-gray-600">Prompt Engineering</p>
                    </div>
                  </div>
                </section>
              </div>

              {/* Columna Derecha */}
              <div>
                {/* Skills Técnicos */}
                <section className="mb-10">
                  <h2 className="text-3xl font-bold text-gray-800 mb-6 pb-2 border-b-4 border-blue-600 inline-block">
                    Skills Técnicos
                  </h2>
                  
                  <div className="mt-6 space-y-2">
                    <h3 className="text-lg font-semibold text-gray-700 mb-4">Lenguajes de Programación</h3>
                    <SkillBar skill="Java" level={65} />
                    <SkillBar skill="Python" level={65} />
                    <SkillBar skill="SQL / MySQL" level={60} />
                  </div>

                  <div className="mt-8 space-y-2">
                    <h3 className="text-lg font-semibold text-gray-700 mb-4">Competencias Técnicas</h3>
                    <SkillBar skill="Desarrollo de Software" level={60} />
                    <SkillBar skill="Bases de Datos" level={60} />
                    <SkillBar skill="Resolución de Problemas" level={70} />
                    <SkillBar skill="Debugging & Testing" level={55} />
                  </div>
                </section>

                {/* Habilidades Blandas */}
                <section className="mb-10">
                  <h2 className="text-3xl font-bold text-gray-800 mb-6 pb-2 border-b-4 border-blue-600 inline-block">
                    Habilidades Blandas
                  </h2>
                  
                  <div className="mt-6 grid grid-cols-1 gap-3">
                    <div className="flex items-center gap-3 bg-gray-50 p-3 rounded-lg">
                      <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                        ✓
                      </div>
                      <span className="text-gray-800 font-medium">Aprendizaje Continuo</span>
                    </div>
                    <div className="flex items-center gap-3 bg-gray-50 p-3 rounded-lg">
                      <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                        ✓
                      </div>
                      <span className="text-gray-800 font-medium">Trabajo en Equipo</span>
                    </div>
                    <div className="flex items-center gap-3 bg-gray-50 p-3 rounded-lg">
                      <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                        ✓
                      </div>
                      <span className="text-gray-800 font-medium">Adaptabilidad</span>
                    </div>
                    <div className="flex items-center gap-3 bg-gray-50 p-3 rounded-lg">
                      <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                        ✓
                      </div>
                      <span className="text-gray-800 font-medium">Pensamiento Analítico</span>
                    </div>
                    <div className="flex items-center gap-3 bg-gray-50 p-3 rounded-lg">
                      <div className="w-10 h-10 bg-blue-600 rounded-full flex items-center justify-center text-white font-bold">
                        ✓
                      </div>
                      <span className="text-gray-800 font-medium">Gestión del Tiempo</span>
                    </div>
                  </div>
                </section>
              </div>
            </div>

            {/* Proyectos Académicos */}
            <section className="mb-10">
              <h2 className="text-3xl font-bold text-gray-800 mb-6 pb-2 border-b-4 border-blue-600 inline-block">
                Proyectos Académicos
              </h2>
              
              <div className="mt-6 grid md:grid-cols-2 gap-6">
                <div className="bg-gradient-to-br from-blue-50 to-blue-100 p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-blue-600 rounded-lg flex items-center justify-center text-white text-2xl flex-shrink-0">
                      🎮
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-gray-800 mb-2">Juego de Bloques (Python)</h3>
                      <p className="text-gray-700 mb-3">
                        Desarrollo de un juego interactivo utilizando Python y Pygame. Implementación de 
                        mecánicas de juego, sistema de puntuación y gestión de colisiones.
                      </p>
                      <div className="flex flex-wrap gap-2">
                        <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full">Python</span>
                        <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full">Pygame</span>
                        <span className="bg-blue-600 text-white text-xs px-3 py-1 rounded-full">POO</span>
                      </div>
                    </div>
                  </div>
                </div>

                <div className="bg-gradient-to-br from-green-50 to-green-100 p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow">
                  <div className="flex items-start gap-4">
                    <div className="w-12 h-12 bg-green-600 rounded-lg flex items-center justify-center text-white text-2xl flex-shrink-0">
                      🗄️
                    </div>
                    <div>
                      <h3 className="text-xl font-bold text-gray-800 mb-2">Sistema de Gestión (Java + MySQL)</h3>
                      <p className="text-gray-700 mb-3">
                        Aplicación de gestión con interfaz gráfica desarrollada en Java. Integración con 
                        base de datos MySQL para operaciones CRUD y manejo de datos persistentes.
                      </p>
                      <div className="flex flex-wrap gap-2">
                        <span className="bg-green-600 text-white text-xs px-3 py-1 rounded-full">Java</span>
                        <span className="bg-green-600 text-white text-xs px-3 py-1 rounded-full">MySQL</span>
                        <span className="bg-green-600 text-white text-xs px-3 py-1 rounded-full">JDBC</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </section>

            {/* Objetivos Profesionales */}
            <section className="mb-6">
              <h2 className="text-3xl font-bold text-gray-800 mb-6 pb-2 border-b-4 border-blue-600 inline-block">
                Objetivos Profesionales
              </h2>
              
              <div className="mt-6 bg-gradient-to-r from-blue-50 to-purple-50 p-6 rounded-xl border-l-4 border-blue-600">
                <ul className="space-y-3 text-gray-700">
                  <li className="flex items-start gap-3">
                    <span className="text-blue-600 font-bold text-xl">→</span>
                    <span>Obtener experiencia práctica en desarrollo de software en un entorno profesional</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-blue-600 font-bold text-xl">→</span>
                    <span>Ampliar conocimientos en frameworks y tecnologías modernas de desarrollo</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-blue-600 font-bold text-xl">→</span>
                    <span>Contribuir a proyectos innovadores aplicando buenas prácticas de programación</span>
                  </li>
                  <li className="flex items-start gap-3">
                    <span className="text-blue-600 font-bold text-xl">→</span>
                    <span>Desarrollar habilidades en trabajo colaborativo y metodologías ágiles</span>
                  </li>
                </ul>
              </div>
            </section>
          </div>

          {/* Footer */}
          <div className="bg-gray-100 p-6 text-center text-gray-600 text-sm">
            <p>Este CV fue generado con React y Tailwind CSS • {new Date().getFullYear()}</p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
