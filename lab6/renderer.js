
class Renderer3D {
    constructor(canvasId) {
        this.canvas = document.getElementById(canvasId);
        this.ctx = this.canvas.getContext('2d');
        
        // Canvas для праекцый
        this.canvasXY = document.getElementById('projectionXY');
        this.ctxXY = this.canvasXY.getContext('2d');
        
        this.canvasXZ = document.getElementById('projectionXZ');
        this.ctxXZ = this.canvasXZ.getContext('2d');
        
        this.canvasYZ = document.getElementById('projectionYZ');
        this.ctxYZ = this.canvasYZ.getContext('2d');
        
        // Налады
        this.scale3D = 50; 
        this.scaleProjection = 25;
        this.offsetX = this.canvas.width / 2;
        this.offsetY = this.canvas.height / 2;
        
        // Стан
        this.showWireframe = true;
        this.showFaces = true;
        this.showVertexLabels = true;
        
        // Колеры
        this.colors = {
            axisX: '#ff5252',
            axisY: '#4caf50',
            axisZ: '#2196f3',
            wireframe: '#ffffff',
            projection: '#8888cc',
            vertexColor: '#ffaa00',
            vertexBorder: '#ff6600',
            vertexLabel: '#ffffff',
            
            faceColors: [
                'rgba(100, 100, 200, 0.7)',   
                'rgba(200, 100, 100, 0.7)',  
                'rgba(100, 200, 100, 0.7)',   
                'rgba(200, 200, 100, 0.7)',   
                'rgba(200, 100, 200, 0.7)',   
                'rgba(100, 200, 200, 0.7)',   
                'rgba(150, 150, 200, 0.7)',   
                'rgba(200, 150, 100, 0.7)',   
                'rgba(150, 200, 150, 0.7)',  
                'rgba(200, 150, 150, 0.7)'    
            ]
        };
    }
    
    // Ачысціць canvas
    clearCanvas(ctx, width, height) {
        ctx.clearRect(0, 0, width, height);
    }
    
    // Намаляваць 3D відарыс
    draw3D(vertices, faces, edges) {
        // Ачысціць canvas
        this.clearCanvas(this.ctx, this.canvas.width, this.canvas.height);
        
        // Намаляваць фон
        this.drawBackground(this.ctx, this.canvas.width, this.canvas.height);
        
        // Намаляваць восі каардынат
        this.drawCoordinateAxes();
        
        if (!vertices || vertices.length === 0) return;
        
        // Пераўтварыць 3D каардынаты ў 2D (ізаметрычная праекцыя)
        const screenPoints = this.project3DTo2D(vertices);
        
        // Намаляваць паверхні (калі ўключана)
        if (this.showFaces && faces) {
            this.drawFaces(screenPoints, faces);
        }
        
        // Намаляваць каркас (калі ўключаны)
        if (this.showWireframe && edges) {
            this.drawWireframe(screenPoints, edges);
        }
        
        // Намаляваць вяршыні
        this.drawVertices(screenPoints);
        
        // Паказаць падпісы вяршынь (калі ўключана)
        if (this.showVertexLabels) {
            this.drawVertexLabels(screenPoints);
        }
    }
    
    project3DTo2D(vertices) {
    const screenPoints = [];
    
    for (let i = 0; i < vertices.length; i++) {
        const vertex = vertices[i];
        // У нас: [x, y, z] дзе x - лева-права, y - глыбіня, z - вышыня
        
        // ПЕРСПЕКТЫЎНАЯ ПРАЕКЦЫЯ з глыбінёй (y) - зараз y глыбіня
        const perspective = 300 / (300 + vertex[1]); // y дадатны - бліжэй
        
        // Зараз: x застаецца x, z стане экранным y (вышынёй)
        const screenX = this.offsetX + vertex[0] * this.scale3D * perspective;
        const screenY = this.offsetY - vertex[2] * this.scale3D * perspective; // z - вышыня
        
        screenPoints.push({
            x: screenX,
            y: screenY,
            original: vertex,
            index: i
        });
    }
    
    return screenPoints;
}
    
    // Намаляваць фон
    drawBackground(ctx, width, height) {
        // Запоўніць фон
        const gradient = ctx.createLinearGradient(0, 0, 0, height);
        gradient.addColorStop(0, '#0a0a1a');
        gradient.addColorStop(1, '#1a1a2e');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, width, height);
        
        // Намаляць сетку
        ctx.strokeStyle = '#2a2a3e';
        ctx.lineWidth = 1;
        
        const gridSize = 20;
        for (let x = 0; x <= width; x += gridSize) {
            ctx.beginPath();
            ctx.moveTo(x, 0);
            ctx.lineTo(x, height);
            ctx.stroke();
        }
        
        for (let y = 0; y <= height; y += gridSize) {
            ctx.beginPath();
            ctx.moveTo(0, y);
            ctx.lineTo(width, y);
            ctx.stroke();
        }
    }
    
    // Намаляваць восі каардынат
    drawCoordinateAxes() {
        const length = 60;
        
        this.ctx.lineCap = 'round';
        
        // Вось X
        this.ctx.strokeStyle = this.colors.axisX;
        this.ctx.lineWidth = 3;
        this.ctx.beginPath();
        this.ctx.moveTo(this.offsetX, this.offsetY);
        this.ctx.lineTo(this.offsetX + length, this.offsetY);
        this.ctx.stroke();
        
        // Вось Y
        this.ctx.strokeStyle = this.colors.axisY;
        this.ctx.beginPath();
        this.ctx.moveTo(this.offsetX, this.offsetY);
        this.ctx.lineTo(this.offsetX, this.offsetY - length);
        this.ctx.stroke();
        
        // Вось Z
        this.ctx.strokeStyle = this.colors.axisZ;
        const zEndX = this.offsetX - length * 0.7;
        const zEndY = this.offsetY + length * 0.7;
        
        this.ctx.beginPath();
        this.ctx.moveTo(this.offsetX, this.offsetY);
        this.ctx.lineTo(zEndX, zEndY);
        this.ctx.stroke();
        
        // Падпісы
        this.ctx.fillStyle = this.colors.axisX;
        this.ctx.font = 'bold 14px Arial';
        this.ctx.fillText('X', this.offsetX + length + 10, this.offsetY + 5);
        
        this.ctx.fillStyle = this.colors.axisY;
        this.ctx.fillText('Z', this.offsetX - 10, this.offsetY - length - 5);
        
        this.ctx.fillStyle = this.colors.axisZ;
        this.ctx.fillText('Y', zEndX - 15, zEndY + 15);
        
        this.ctx.lineCap = 'butt';
    }
    
    drawFaces(screenPoints, faces) {
    // Сартаваць грани па СЯРЭДНЯЙ ГЛЫБІНІ (зараз y - глыбіня)
    const facesWithDepth = [];
    
    for (let i = 0; i < faces.length; i++) {
        const face = faces[i];
        if (face.length < 3) continue;
        
        let totalDepth = 0;
        const points = [];
        
        for (const vertexIdx of face) {
            if (vertexIdx < screenPoints.length) {
                const point = screenPoints[vertexIdx];
                points.push(point);
                // Разлічыць глыбіню - y-каардыната (зараз y - глыбіня)
                totalDepth += point.original[1]; // y - глыбіня
            }
        }
        
        if (points.length >= 3) {
            const avgDepth = totalDepth / points.length;
            facesWithDepth.push({
                index: i,
                points: points,
                depth: avgDepth
            });
        }
    }
    
    facesWithDepth.sort((a, b) => b.depth - a.depth);
    
    for (const faceData of facesWithDepth) {
        const colorIndex = faceData.index % this.colors.faceColors.length;
        
        this.ctx.fillStyle = this.colors.faceColors[colorIndex];
        this.ctx.beginPath();
        this.ctx.moveTo(faceData.points[0].x, faceData.points[0].y);
        
        for (let j = 1; j < faceData.points.length; j++) {
            this.ctx.lineTo(faceData.points[j].x, faceData.points[j].y);
        }
        
        this.ctx.closePath();
        this.ctx.fill();
        
        this.ctx.strokeStyle = this.colors.faceColors[colorIndex].replace('0.7', '0.9');
        this.ctx.lineWidth = 1.5;
        this.ctx.stroke();
    }
}
    
    drawWireframe(screenPoints, edges) {
        this.ctx.strokeStyle = this.colors.wireframe;
        this.ctx.lineWidth = 2;
        this.ctx.lineCap = 'round';
        
        for (const edge of edges) {
            if (edge[0] < screenPoints.length && edge[1] < screenPoints.length) {
                const p1 = screenPoints[edge[0]];
                const p2 = screenPoints[edge[1]];
                
                this.ctx.beginPath();
                this.ctx.moveTo(p1.x, p1.y);
                this.ctx.lineTo(p2.x, p2.y);
                this.ctx.stroke();
            }
        }
        
        this.ctx.lineCap = 'butt';
    }
    
    drawVertices(screenPoints) {
        for (const point of screenPoints) {
            this.ctx.fillStyle = this.colors.vertexColor;
            this.ctx.beginPath();
            this.ctx.arc(point.x, point.y, 4, 0, Math.PI * 2);
            this.ctx.fill();
            
            this.ctx.strokeStyle = this.colors.vertexBorder;
            this.ctx.lineWidth = 2;
            this.ctx.beginPath();
            this.ctx.arc(point.x, point.y, 4, 0, Math.PI * 2);
            this.ctx.stroke();
        }
    }
    
    drawVertexLabels(screenPoints) {
        this.ctx.fillStyle = this.colors.vertexLabel;
        this.ctx.font = 'bold 12px Arial';
        this.ctx.textAlign = 'center';
        this.ctx.textBaseline = 'middle';
        
        const vertexLetters = ['A', 'B', 'M', 'O', 'N', 'P', 'Q', 'K', 
                              'E', 'C', 'D', 'F', 'G', 'I', 'L', 'J'];
        
        for (let i = 0; i < screenPoints.length; i++) {
            const point = screenPoints[i];
            const letter = vertexLetters[i] || i.toString();
            
            this.ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
            this.ctx.fillRect(point.x - 10, point.y - 18, 20, 15);
            
            this.ctx.fillStyle = this.colors.vertexLabel;
            this.ctx.fillText(letter, point.x, point.y - 10);
            
            this.ctx.font = '9px Arial';
            this.ctx.fillText(`(${i})`, point.x, point.y + 15);
            this.ctx.font = 'bold 12px Arial';
        }
    }
    
   drawProjections(projectionXY, projectionXZ, projectionYZ, edges) {
    const projWidth = this.canvasXY.width;
    const projHeight = this.canvasXY.height;
    
    this.drawSingleProjection(this.ctxXY, projectionXY, edges, projWidth, projHeight, 'XZ (Зверху)'); // Было XY
    this.drawSingleProjection(this.ctxXZ, projectionXZ, edges, projWidth, projHeight, 'XY (Спераду)'); // Было XZ
    this.drawSingleProjection(this.ctxYZ, projectionYZ, edges, projWidth, projHeight, 'YZ (Збоку)');
}
    
    drawSingleProjection(ctx, points, edges, width, height, title) {
    this.clearCanvas(ctx, width, height);
    
    ctx.fillStyle = '#2d2d4d';
    ctx.fillRect(0, 0, width, height);
    
    ctx.strokeStyle = '#4a4a6d';
    ctx.lineWidth = 2;
    ctx.strokeRect(1, 1, width - 2, height - 2);
    
    ctx.fillStyle = '#ffffff';
    ctx.font = 'bold 12px Arial';
    ctx.textAlign = 'center';
    
    const centerX = width / 2;
    const centerY = height / 2;
    
    if (!points || points.length === 0) return;
    
    const screenPoints = [];
    for (const p of points) {
        const screenX = centerX + p[0] * this.scaleProjection;
        const screenY = centerY - p[1] * this.scaleProjection;
        screenPoints.push({ x: screenX, y: screenY });
    }
    
    ctx.strokeStyle = '#666699';
    ctx.lineWidth = 1;
    ctx.fillStyle = '#cccccc';
    ctx.font = '10px Arial';
    
    if (title.includes('XY')) {
        ctx.beginPath();
        ctx.moveTo(20, centerY);
        ctx.lineTo(width - 20, centerY);
        ctx.stroke();
        ctx.fillText('X', width - 15, centerY + 12);
        
        ctx.beginPath();
        ctx.moveTo(centerX, 20);
        ctx.lineTo(centerX, height - 20);
        ctx.stroke();
        ctx.fillText('Z', centerX + 5, 15);
    } 
    else if (title.includes('XZ')) {
        ctx.beginPath();
        ctx.moveTo(20, centerY);
        ctx.lineTo(width - 20, centerY);
        ctx.stroke();
        ctx.fillText('X', width - 15, centerY + 12);
        
        ctx.beginPath();
        ctx.moveTo(centerX, 20);
        ctx.lineTo(centerX, height - 20);
        ctx.stroke();
        ctx.fillText('Y', centerX + 5, 15); 
    }
    else if (title.includes('YZ')) {
        ctx.beginPath();
        ctx.moveTo(20, centerY);
        ctx.lineTo(width - 20, centerY);
        ctx.stroke();
        ctx.fillText('Y', width - 15, centerY + 12);
        
        ctx.beginPath();
        ctx.moveTo(centerX, 20);
        ctx.lineTo(centerX, height - 20);
        ctx.stroke();
        ctx.fillText('Z', centerX + 5, 15); 
    }
    
    // Намаляваць рэбры
    ctx.strokeStyle = this.colors.projection;
    ctx.lineWidth = 2;
    
    for (const edge of edges) {
        if (edge[0] < screenPoints.length && edge[1] < screenPoints.length) {
            const p1 = screenPoints[edge[0]];
            const p2 = screenPoints[edge[1]];
            
            ctx.beginPath();
            ctx.moveTo(p1.x, p1.y);
            ctx.lineTo(p2.x, p2.y);
            ctx.stroke();
        }
    }
    
    // Намаляваць вяршыні
    for (const point of screenPoints) {
        ctx.fillStyle = this.colors.vertexColor;
        ctx.beginPath();
        ctx.arc(point.x, point.y, 3, 0, Math.PI * 2);
        ctx.fill();
    }
}
    
    // Пераключыць рэжым каркас/поверхня
    toggleWireframe() {
        this.showWireframe = !this.showWireframe;
        return this.showWireframe;
    }
    
    // Пераключыць адлюстраванне паверхняў
    toggleFaces() {
        this.showFaces = !this.showFaces;
        return this.showFaces;
    }
    
    // Пераключыць падпісы вяршынь
    toggleVertexLabels() {
        this.showVertexLabels = !this.showVertexLabels;
        return this.showVertexLabels;
    }
    
    // Абнавіць памеры canvas
    updateCanvasSize() {
        this.offsetX = this.canvas.width / 2;
        this.offsetY = this.canvas.height / 2;
    }
}

window.Renderer3D = Renderer3D;