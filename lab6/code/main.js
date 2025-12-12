class MainApp {
    constructor() {
        // Ініцыялізацыя кампанентаў
        this.letter3D = window.Letter3D;
        this.transformations = new window.Transformations3D();
        this.renderer = new window.Renderer3D('mainCanvas');
        
        // Стан праграмы
        this.isWireframe = true;
        this.isFaces = true;
        
        // Ініцыялізацыя
        this.init();
        this.bindEvents();
        this.updateAll();
        this.updateViewSliders();
    }
    
     updateViewSliders() {
        // Усталяваць пачатковыя значэнні слайдэраў выгляду
        document.getElementById('rotateX').value = this.transformations.viewRotation.x;
        document.getElementById('rotateY').value = this.transformations.viewRotation.y;
        document.getElementById('rotateZ').value = this.transformations.viewRotation.z;
    }

    // Ініцыялізацыя праграмы
    init() {
        // Абнавіць інфармацыю
        this.updateInfo();
        
        // Абнавіць значэнні на слайдахэрах
        this.updateSliderValues();
        
        // Абнавіць матрыцу
        this.updateMatrixDisplay();
    }
    
    // Звязаць падзеі
    bindEvents() {
        document.getElementById('toggleLabels').addEventListener('click', () => {
            this.renderer.toggleVertexLabels();
            this.updateAll();
        });

        // Кнопкі кіравання выглядам
        document.getElementById('resetView').addEventListener('click', () => {
            this.transformations.setViewRotation(30, 45, 0);
            this.updateViewSliders();
            this.updateAll();
        });
        
        document.getElementById('toggleWireframe').addEventListener('click', () => {
            this.isWireframe = this.renderer.toggleWireframe();
            this.updateAll();
        });
        
        // Слайдэры для выгляду
        document.getElementById('rotateX').addEventListener('input', (e) => {
            this.transformations.viewRotation.x = parseInt(e.target.value);
            this.updateAll();
        });
        
        document.getElementById('rotateY').addEventListener('input', (e) => {
            this.transformations.viewRotation.y = parseInt(e.target.value);
            this.updateAll();
        });
        
        document.getElementById('rotateZ').addEventListener('input', (e) => {
            this.transformations.viewRotation.z = parseInt(e.target.value);
            this.updateAll();
        });
        
        // Слайдэры для маштабавання
        document.getElementById('scaleX').addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('scaleXValue').textContent = value.toFixed(1);
            this.transformations.scale.x = value;
            this.updateAll();
        });
        
        document.getElementById('scaleY').addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('scaleYValue').textContent = value.toFixed(1);
            this.transformations.scale.y = value;
            this.updateAll();
        });
        
        document.getElementById('scaleZ').addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('scaleZValue').textContent = value.toFixed(1);
            this.transformations.scale.z = value;
            this.updateAll();
        });
        
        document.getElementById('resetScale').addEventListener('click', () => {
            this.transformations.resetScale();
            document.getElementById('scaleX').value = 1;
            document.getElementById('scaleY').value = 1;
            document.getElementById('scaleZ').value = 1;
            
            document.getElementById('scaleXValue').textContent = '1.0';
            document.getElementById('scaleYValue').textContent = '1.0';
            document.getElementById('scaleZValue').textContent = '1.0';
            
            this.updateAll();
        });
        
        // Слайдэры для пераносу
        document.getElementById('translateX').addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('translateXValue').textContent = value.toFixed(1);
            this.transformations.translate.x = value;
            this.updateAll();
        });
        
        document.getElementById('translateY').addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('translateYValue').textContent = value.toFixed(1);
            this.transformations.translate.y = value;
            this.updateAll();
        });
        
        document.getElementById('translateZ').addEventListener('input', (e) => {
            const value = parseFloat(e.target.value);
            document.getElementById('translateZValue').textContent = value.toFixed(1);
            this.transformations.translate.z = value;
            this.updateAll();
        });
        
        document.getElementById('resetTranslate').addEventListener('click', () => {
            this.transformations.resetTranslate();
            document.getElementById('translateX').value = 0;
            document.getElementById('translateY').value = 0;
            document.getElementById('translateZ').value = 0;
            
            document.getElementById('translateXValue').textContent = '0.0';
            document.getElementById('translateYValue').textContent = '0.0';
            document.getElementById('translateZValue').textContent = '0.0';
            
            this.updateAll();
        });
        
        document.getElementById('rotateAxisX').addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            document.getElementById('rotateAxisXValue').textContent = value + '°';
            this.transformations.rotate.x = value;
            this.updateAll();
        });
        
        document.getElementById('rotateAxisY').addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            document.getElementById('rotateAxisYValue').textContent = value + '°';
            this.transformations.rotate.y = value;
            this.updateAll();
        });
        
        document.getElementById('rotateAxisZ').addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            document.getElementById('rotateAxisZValue').textContent = value + '°';
            this.transformations.rotate.z = value;
            this.updateAll();
        });
        
        document.getElementById('resetRotation').addEventListener('click', () => {
            this.transformations.resetRotation();
            document.getElementById('rotateAxisX').value = 0;
            document.getElementById('rotateAxisY').value = 0;
            document.getElementById('rotateAxisZ').value = 0;
            document.getElementById('customRotate').value = 0;
            
            document.getElementById('rotateAxisXValue').textContent = '0°';
            document.getElementById('rotateAxisYValue').textContent = '0°';
            document.getElementById('rotateAxisZValue').textContent = '0°';
            document.getElementById('customRotateValue').textContent = '0°';
            
            this.updateAll();
        });
        
        document.getElementById('customRotate').addEventListener('input', (e) => {
            const value = parseInt(e.target.value);
            document.getElementById('customRotateValue').textContent = value + '°';
            this.transformations.customAngle = value;
            this.updateAll();
        });
        
        document.getElementById('applyCustomRotation').addEventListener('click', () => {
            const axisX = parseFloat(document.getElementById('axisX').value);
            const axisY = parseFloat(document.getElementById('axisY').value);
            const axisZ = parseFloat(document.getElementById('axisZ').value);
            
            this.transformations.setCustomRotation([axisX, axisY, axisZ], this.transformations.customAngle);
            this.updateAll();
        });
        
        // Кнопка скіду ўсіх пераўтварэнняў
        document.getElementById('resetAll').addEventListener('click', () => {
            this.transformations.resetAll();
            this.resetAllSliders();
            this.updateAll();
        });
        
        // Абнаўленне памеру акна
        window.addEventListener('resize', () => {
            this.renderer.updateCanvasSize();
            this.updateAll();
        });
    }
    
    // Абнавіць усё адлюстраванне
    updateAll() {
        // Ужыць пераўтварэнні
        const transformedVertices = this.transformations.applyTransformations(
            this.transformations.originalVertices  // Выкарыстоўваем ужо павернутыя!
        );

        // Намаляваць 3D відарыс
        this.renderer.draw3D(transformedVertices, this.letter3D.faces, this.letter3D.edges);
        
        // Атрымаць праекцыі
        const projectionXY = this.transformations.getProjections(transformedVertices, 'xy');
        const projectionXZ = this.transformations.getProjections(transformedVertices, 'xz');
        const projectionYZ = this.transformations.getProjections(transformedVertices, 'yz');
        
        // Намаляваць праекцыі
        this.renderer.drawProjections(projectionXY, projectionXZ, projectionYZ, this.letter3D.edges);
        
        // Абнавіць матрыцу
        this.updateMatrixDisplay();
        
        // Абнавіць статус
        this.updateStatus('Гатова');
    }
    
    updateViewSliders() {
        document.getElementById('rotateX').value = this.transformations.viewRotation.x;
        document.getElementById('rotateY').value = this.transformations.viewRotation.y;
        document.getElementById('rotateZ').value = this.transformations.viewRotation.z;
    }
    
    updateSliderValues() {
        document.getElementById('scaleXValue').textContent = this.transformations.scale.x.toFixed(1);
        document.getElementById('scaleYValue').textContent = this.transformations.scale.y.toFixed(1);
        document.getElementById('scaleZValue').textContent = this.transformations.scale.z.toFixed(1);
        
        document.getElementById('scaleX').value = this.transformations.scale.x;
        document.getElementById('scaleY').value = this.transformations.scale.y;
        document.getElementById('scaleZ').value = this.transformations.scale.z;
        
        document.getElementById('translateXValue').textContent = this.transformations.translate.x.toFixed(1);
        document.getElementById('translateYValue').textContent = this.transformations.translate.y.toFixed(1);
        document.getElementById('translateZValue').textContent = this.transformations.translate.z.toFixed(1);
        
        document.getElementById('translateX').value = this.transformations.translate.x;
        document.getElementById('translateY').value = this.transformations.translate.y;
        document.getElementById('translateZ').value = this.transformations.translate.z;
        
        document.getElementById('rotateAxisXValue').textContent = this.transformations.rotate.x + '°';
        document.getElementById('rotateAxisYValue').textContent = this.transformations.rotate.y + '°';
        document.getElementById('rotateAxisZValue').textContent = this.transformations.rotate.z + '°';
        
        document.getElementById('rotateAxisX').value = this.transformations.rotate.x;
        document.getElementById('rotateAxisY').value = this.transformations.rotate.y;
        document.getElementById('rotateAxisZ').value = this.transformations.rotate.z;
        
        this.updateViewSliders();
    }
    
    // Скінуць усе слайдэры
    resetAllSliders() {
        this.transformations.resetAll();
        
        // Абнавіць адлюстраванне слайдэраў
        this.updateSliderValues();
        
        // Адвольная вось
        document.getElementById('axisX').value = 1;
        document.getElementById('axisY').value = 1;
        document.getElementById('axisZ').value = 1;
        document.getElementById('customRotate').value = 0;
        document.getElementById('customRotateValue').textContent = '0°';
    }
    
    // Абнавіць адлюстраванне матрыцы
    updateMatrixDisplay() {
        const matrixString = this.transformations.getMatrixString();
        const matrixElement = document.getElementById('transformationMatrix');
        
        // Падзяліць матрыцу на радкі
        const rows = matrixString.trim().split('\n');
        
        // Ачысціць і абнавіць
        matrixElement.innerHTML = '';
        for (const row of rows) {
            const div = document.createElement('div');
            div.textContent = row;
            matrixElement.appendChild(div);
        }
    }
    
    // Абнавіць інфармацыю
    updateInfo() {
        document.getElementById('vertexCount').textContent = this.letter3D.getVertexCount();
        document.getElementById('faceCount').textContent = this.letter3D.getFaceCount();
        document.getElementById('edgeCount').textContent = this.letter3D.getEdgeCount();
        
        const infoDiv = document.getElementById('status');
        infoDiv.innerHTML = `
            <strong>Літара "П" па дакладных каардынатах</strong><br>
            • 16 вяршынь (A, B, M, O, N, P, Q, K, E, C, D, F, G, I, L, J)<br>
            • 10 мнагавугольнікаў<br>
            • z-каардынаты: 0 (зад), 4-5 (пярэд)
        `;
}
    
    // Абнавіць статус
    updateStatus(status) {
        document.getElementById('status').textContent = status;
    }
}

// Запусціць праграму пры загрузцы
window.addEventListener('DOMContentLoaded', () => {
    new MainApp();
});