import os
from flask import Flask, render_template_string, request, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Configuración de carpetas para archivos subidos
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Lista en memoria para soluciones dinámicas subidas por los usuarios
soluciones_list = [
    {
        "titulo": "Rastrillo-Pala de Arrastre Ergonómico",
        "descripcion": "Diseñado para movilizar grandes volúmenes de lodo semi-húmedo en pasillos y habitaciones reducidas sin requerir levantar todo el peso verticalmente.",
        "costo": "$15 - $25 USD",
        "categoria": "Herramienta Manual",
        "imagen": "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"
    },
    {
        "titulo": "Hidro-Extractor Venturi Comunitario",
        "descripcion": "Dispositivo hidráulico portátil que utiliza presión de agua externa para generar succión por vacío, permitiendo extraer lodo fluido en esquinas complejas.",
        "costo": "$40 - $70 USD",
        "categoria": "Succión / Hidráulico",
        "imagen": "https://images.unsplash.com/photo-1547683905-f686c993aae5?auto=format&fit=crop&w=600&q=80"
    }
]

# Estado global de archivos subidos
archivos_estado = {
    "informe_pdf": None,
    "informe_financiero": None,
    "youtube_id": "dQw4w9WgXcQ"
}

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Remoción de Barro - Rally Latinoamericano de Innovación</title>
    <!-- Bootstrap 5 CSS -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <!-- FontAwesome Icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <style>
        :root {
            --primary-color: #2c3e50;
            --accent-color: #e67e22;
            --dark-mud: #3e2723;
        }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f4f6f9;
            color: #333;
        }
        header {
            background: linear-gradient(135deg, var(--primary-color), var(--dark-mud));
            color: white;
            padding: 50px 0;
        }
        .card-custom {
            border: none;
            border-radius: 12px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            transition: transform 0.2s ease;
        }
        .card-custom:hover {
            transform: translateY(-3px);
        }
        .badge-team {
            background-color: var(--accent-color);
            color: white;
        }
        .video-container {
            position: relative;
            padding-bottom: 56.25%;
            height: 0;
            overflow: hidden;
            border-radius: 12px;
            background-color: #000;
        }
        .video-container iframe {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            border: 0;
        }
        .pdf-preview {
            width: 100%;
            height: 450px;
            border: 1px solid #ddd;
            border-radius: 8px;
        }
        footer {
            background-color: var(--primary-color);
            color: white;
            padding: 25px 0;
            margin-top: 50px;
        }
    </style>
</head>
<body>

    <!-- Header / Hero Section -->
    <header class="text-center">
        <div class="container">
            <span class="badge badge-team px-3 py-2 rounded-pill mb-3 fw-bold">Rally Latinoamericano de Innovación 2026</span>
            <h1 class="display-5 fw-bold">Remoción y Extracción de Barro en Viviendas Anegadas</h1>
            <p class="lead mt-2 text-light">Sistema integral de herramientas portátiles, informes técnicos e impacto comunitario.</p>
        </div>
    </header>

    <main class="container my-5">

        <!-- INFORMACIÓN DEL EQUIPO -->
        <section class="mb-5">
            <div class="card card-custom p-4 bg-white border-start border-4 border-warning">
                <div class="row align-items-center">
                    <div class="col-md-8">
                        <h3 class="fw-bold text-dark"><i class="fas fa-users text-warning me-2"></i> Equipo: ELCONOCIMIENTOESPODER</h3>
                        <p class="text-muted mb-1"><strong>Sede:</strong> UNER CONCORDIA — Argentina 🇦🇷</p>
                        <p class="small text-secondary mb-0">Desafío 06: Remoción y extracción de barro en viviendas anegadas post-aluvión.</p>
                    </div>
                    <div class="col-md-4 text-md-end mt-3 mt-md-0">
                        <span class="badge bg-success p-2 fs-6">9 Integrantes</span>
                    </div>
                </div>
                <hr class="my-3">
                <div class="table-responsive">
                    <table class="table table-sm table-striped mb-0">
                        <thead>
                            <tr class="table-dark">
                                <th>#</th>
                                <th>Participante</th>
                                <th>Estatus</th>
                                <th>Área de Estudio</th>
                                <th>Modalidad</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr><td>1</td><td>⭐ HILARIO MANUEL CARABALLO</td><td>Líder</td><td>Administración</td><td>Presencial</td></tr>
                            <tr><td>2</td><td>ENZO MACIEL</td><td>Integrante</td><td>Ingeniería</td><td>Presencial</td></tr>
                            <tr><td>3</td><td>VALENTINO GIOVENALE</td><td>Integrante</td><td>Ingeniería</td><td>Presencial</td></tr>
                            <tr><td>4</td><td>MARTINIANO GODOY</td><td>Integrante</td><td>Ingeniería</td><td>Presencial</td></tr>
                            <tr><td>5</td><td>GABRIEL MORENO</td><td>Integrante</td><td>Ingeniería</td><td>Presencial</td></tr>
                            <tr><td>6</td><td>TOMAS HUDSON</td><td>Integrante</td><td>Administración</td><td>Presencial</td></tr>
                            <tr><td>7</td><td>TOMÁS SILVETTI</td><td>Integrante</td><td>Administración</td><td>Presencial</td></tr>
                            <tr><td>8</td><td>LARA RODRÍGUEZ</td><td>Integrante</td><td>Economía - Contabilidad</td><td>Presencial</td></tr>
                            <tr><td>9</td><td>GUADALUPE RICHARD</td><td>Integrante</td><td>Economía - Contabilidad</td><td>Presencial</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- MÓDULO 1: INFORMES PDF Y MULTIMEDIA -->
        <section class="mb-5">
            <h2 class="fw-bold mb-4 text-dark"><i class="fas fa-file-pdf text-danger me-2"></i> Entregables Oficiales & Documentación</h2>
            <div class="row g-4">
                
                <!-- Informe Técnico PDF -->
                <div class="col-lg-6">
                    <div class="card card-custom h-100 p-4 bg-white border-top border-4 border-danger">
                        <h4 class="fw-bold text-dark"><i class="fas fa-file-alt text-danger me-2"></i> Informe Técnico Principal (PDF)</h4>
                        <p class="text-muted small">Carga el informe final con la justificación operativa, metodologías y estandarización.</p>
                        
                        <form action="/upload_pdf" method="post" enctype="multipart/form-data" class="mb-3">
                            <input type="hidden" name="tipo_doc" value="informe_pdf">
                            <div class="input-group input-group-sm">
                                <input type="file" name="archivo" class="form-control" accept=".pdf" required>
                                <button class="btn btn-danger" type="submit"><i class="fas fa-upload me-1"></i> Cargar PDF</button>
                            </div>
                        </form>

                        {% if archivos.informe_pdf %}
                            <div class="alert alert-success py-2 px-3 small d-flex justify-content-between align-items-center">
                                <span><i class="fas fa-check-circle me-1"></i> {{ archivos.informe_pdf }}</span>
                                <a href="/uploads/{{ archivos.informe_pdf }}" target="_blank" class="btn btn-sm btn-outline-success">Ver Documento</a>
                            </div>
                            <iframe src="/uploads/{{ archivos.informe_pdf }}" class="pdf-preview mt-2"></iframe>
                        {% else %}
                            <div class="alert alert-secondary text-center py-4 text-muted small">
                                <i class="fas fa-file-upload fa-2x mb-2 d-block"></i>
                                Ningún Informe Técnico subido todavía.
                            </div>
                        {% endif %}
                    </div>
                </div>

                <!-- Informe Financiero PDF -->
                <div class="col-lg-6">
                    <div class="card card-custom h-100 p-4 bg-white border-top border-4 border-success">
                        <h4 class="fw-bold text-dark"><i class="fas fa-calculator text-success me-2"></i> Informe Financiero & Costos (PDF)</h4>
                        <p class="text-muted small">Carga la estructura de costos de fabricación local y presupuesto de escalabilidad.</p>
                        
                        <form action="/upload_pdf" method="post" enctype="multipart/form-data" class="mb-3">
                            <input type="hidden" name="tipo_doc" value="informe_financiero">
                            <div class="input-group input-group-sm">
                                <input type="file" name="archivo" class="form-control" accept=".pdf" required>
                                <button class="btn btn-success" type="submit"><i class="fas fa-upload me-1"></i> Cargar PDF</button>
                            </div>
                        </form>

                        {% if archivos.informe_financiero %}
                            <div class="alert alert-success py-2 px-3 small d-flex justify-content-between align-items-center">
                                <span><i class="fas fa-check-circle me-1"></i> {{ archivos.informe_financiero }}</span>
                                <a href="/uploads/{{ archivos.informe_financiero }}" target="_blank" class="btn btn-sm btn-outline-success">Ver Documento</a>
                            </div>
                            <iframe src="/uploads/{{ archivos.informe_financiero }}" class="pdf-preview mt-2"></iframe>
                        {% else %}
                            <div class="alert alert-secondary text-center py-4 text-muted small">
                                <i class="fas fa-file-upload fa-2x mb-2 d-block"></i>
                                Ningún Informe Financiero subido todavía.
                            </div>
                        {% endif %}
                    </div>
                </div>

            </div>
        </section>

        <!-- MÓDULO 2: PITCH YOUTUBE -->
        <section class="mb-5">
            <div class="card card-custom p-4 bg-white border-top border-4 border-primary">
                <div class="row align-items-center mb-3">
                    <div class="col-md-7">
                        <h3 class="fw-bold text-dark mb-1"><i class="fab fa-youtube text-danger me-2"></i> Video Pitch Oficial (YouTube)</h3>
                        <p class="text-muted small mb-0">Video de 2 minutos exigido por la competencia.</p>
                    </div>
                    <div class="col-md-5">
                        <form action="/update_youtube" method="post" class="mt-2 mt-md-0">
                            <div class="input-group input-group-sm">
                                <input type="text" name="youtube_url" class="form-control" placeholder="Pegar Link o ID de YouTube" required>
                                <button class="btn btn-primary" type="submit"><i class="fas fa-sync-alt me-1"></i> Actualizar</button>
                            </div>
                        </form>
                    </div>
                </div>
                <div class="video-container">
                    <iframe src="https://www.youtube.com/embed/{{ archivos.youtube_id }}" allowfullscreen></iframe>
                </div>
            </div>
        </section>

        <!-- MÓDULO 3: SOLUCIONES PROPUESTAS (CARGA DINÁMICA) -->
        <section class="mb-5">
            <div class="d-flex justify-content-between align-items-center mb-4">
                <h2 class="fw-bold text-dark mb-0"><i class="fas fa-lightbulb text-warning me-2"></i> Soluciones & Dispositivos Desarrollados</h2>
                <button class="btn btn-warning fw-bold text-dark btn-sm" data-bs-toggle="modal" data-bs-target="#modalSolucion">
                    <i class="fas fa-plus-circle me-1"></i> Cargar Nueva Solución
                </button>
            </div>

            <div class="row g-4">
                {% for sol in soluciones %}
                <div class="col-md-6 col-lg-4">
                    <div class="card card-custom h-100 bg-white">
                        <img src="{{ sol.imagen }}" class="card-img-top" alt="{{ sol.titulo }}" style="height: 200px; object-fit: cover;">
                        <div class="card-body">
                            <span class="badge bg-secondary mb-2">{{ sol.categoria }}</span>
                            <h5 class="card-title fw-bold text-dark">{{ sol.titulo }}</h5>
                            <p class="card-text text-muted small">{{ sol.descripcion }}</p>
                        </div>
                        <div class="card-footer bg-light border-0 d-flex justify-content-between align-items-center">
                            <span class="small fw-bold text-success"><i class="fas fa-tag me-1"></i> {{ sol.costo }}</span>
                            <span class="badge bg-light text-dark border">Fabricación Local</span>
                        </div>
                    </div>
                </div>
                {% endfor %}
            </div>
        </section>

    </main>

    <!-- MODAL PARA CARGAR NUEVA SOLUCIÓN CON MULTIMEDIA -->
    <div class="modal fade" id="modalSolucion" tabindex="-1" aria-hidden="true">
        <div class="modal-dialog">
            <div class="modal-content">
                <form action="/add_solucion" method="post" enctype="multipart/form-data">
                    <div class="modal-header bg-warning">
                        <h5 class="modal-title fw-bold text-dark"><i class="fas fa-tools me-2"></i> Agregar Nueva Solución / Dispositivo</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close"></button>
                    </div>
                    <div class="modal-body">
                        <div class="mb-3">
                            <label class="form-label fw-bold">Nombre del Dispositivo / Solución</label>
                            <input type="text" name="titulo" class="form-control form-control-sm" required placeholder="Ej. Pala Eyectora Manual">
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Categoría</label>
                            <select name="categoria" class="form-select form-select-sm">
                                <option value="Herramienta Manual">Herramienta Manual</option>
                                <option value="Succión / Hidráulico">Succión / Hidráulico</option>
                                <option value="Dispositivo Mecánico">Dispositivo Mecánico</option>
                                <option value="Estrategia Comunitaria">Estrategia Comunitaria</option>
                            </select>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Descripción Operativa</label>
                            <textarea name="descripcion" class="form-control form-control-sm" rows="3" required placeholder="Explica cómo funciona en espacios reducidos..."></textarea>
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Costo Estimado de Fabricación</label>
                            <input type="text" name="costo" class="form-control form-control-sm" required placeholder="Ej. $20 USD">
                        </div>
                        <div class="mb-3">
                            <label class="form-label fw-bold">Foto / Imagen Multimedia</label>
                            <input type="file" name="foto_solucion" class="form-control form-control-sm" accept="image/*" required>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button type="button" class="btn btn-secondary btn-sm" data-bs-dismiss="modal">Cancelar</button>
                        <button type="submit" class="btn btn-warning btn-sm fw-bold">Guardar Solución</button>
                    </div>
                </form>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="text-center">
        <div class="container">
            <p class="mb-0">&copy; 2026 - Equipo ELCONOCIMIENTOESPODER | Sede UNER Concordia | Rally Latinoamericano de Innovación</p>
        </div>
    </footer>

    <!-- Bootstrap 5 JS Bundle -->
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE, soluciones=soluciones_list, archivos=archivos_estado)

# Ruta para descargar/ver PDFs subidos
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Ruta para subir Informes PDF
@app.route('/upload_pdf', methods=['POST'])
def upload_pdf():
    tipo_doc = request.form.get('tipo_doc')
    if 'archivo' in request.files:
        file = request.files['archivo']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            archivos_estado[tipo_doc] = filename
    return redirect(url_for('home'))

# Ruta para actualizar enlace de YouTube
@app.route('/update_youtube', methods=['POST'])
def update_youtube():
    url = request.form.get('youtube_url', '')
    if 'v=' in url:
        yt_id = url.split('v=')[1].split('&')[0]
    elif 'youtu.be/' in url:
        yt_id = url.split('youtu.be/')[1].split('?')[0]
    else:
        yt_id = url
    archivos_estado['youtube_id'] = yt_id
    return redirect(url_for('home'))

# Ruta para agregar nueva solución con imagen subida por el usuario
@app.route('/add_solucion', methods=['POST'])
def add_solucion():
    titulo = request.form.get('titulo')
    categoria = request.form.get('categoria')
    descripcion = request.form.get('descripcion')
    costo = request.form.get('costo')
    
    img_url = "https://images.unsplash.com/photo-1584467735811-9985103cb136?auto=format&fit=crop&w=600&q=80"
    if 'foto_solucion' in request.files:
        file = request.files['foto_solucion']
        if file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            img_url = f"/uploads/{filename}"

    soluciones_list.append({
        "titulo": titulo,
        "categoria": categoria,
        "descripcion": descripcion,
        "costo": costo,
        "imagen": img_url
    })
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)