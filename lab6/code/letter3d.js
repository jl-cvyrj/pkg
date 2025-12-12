const letterPVertices = [
    // z = -3 (задняя плоскасць)
    [0.5, 1, -3],    // 0: A(0.5, 1, -3)
    [1.5, 1, -3],    // 1: B(1.5, 1, -3)
    [0.5, -1, -3],   // 2: M(0.5, -1, -3)
    [1.5, -1, -3],   // 3: O(1.5, -1, -3)
    
    [-0.5, 1, -3],   // 4: N(-0.5, 1, -3)
    [-1.5, 1, -3],   // 5: P(-1.5, 1, -3)
    [-1.5, -1, -3],  // 6: Q(-1.5, -1, -3)
    [-0.5, -1, -3],  // 7: K(-0.5, -1, -3)
    
    // z = 1 (сярэдняя частка)
    [-0.5, -1, 1],   // 8: E(-0.5, -1, 1)
    [0.5, -1, 1],    // 9: C(0.5, -1, 1)
    [-0.5, 1, 1],    // 10: D(-0.5, 1, 1)
    [0.5, 1, 1],     // 11: F(0.5, 1, 1)
    
    // z = 2 (пярэдняя частка)
    [-1.5, 1, 2],    // 12: G(-1.5, 1, 2)
    [1.5, 1, 2],     // 13: I(1.5, 1, 2)
    [1.5, -1, 2],    // 14: L(1.5, -1, 2)
    [-1.5, -1, 2]    // 15: J(-1.5, -1, 2)
];

const letterPFaces = [
    // ABOM
    [0, 1, 3, 2],
    
    // PNKQ
    [5, 4, 7, 6],
    
    // CFAM
    [9, 11, 0, 2],
    
    // DEKN
    [10, 8, 7, 4],
    
    // ECDF
    [8, 9, 11, 10],
    
    // ILOB
    [13, 14, 3, 1],
    
    // GJQP
    [12, 15, 6, 5],
    
    // JGIL
    [15, 12, 13, 14],
    
    // QKECMOLJ
    [6, 7, 8, 9, 2, 3, 14, 15],
    
    // BAFDNPGI
    [1, 0, 11, 10, 4, 5, 12, 13]
];

// Рэбры для каркаснай мадэлі
const letterPEdges = [
    // ABOM
    [0, 1], [1, 3], [3, 2], [2, 0],
    
    // PNKQ
    [5, 4], [4, 7], [7, 6], [6, 5],
    
    // CFAM
    [9, 11], [11, 0], [0, 2], [2, 9],
    
    // DEKN
    [10, 8], [8, 7], [7, 4], [4, 10],
    
    // ECDF
    [8, 9], [9, 11], [11, 10], [10, 8],
    
    // ILOB
    [13, 14], [14, 3], [3, 1], [1, 13],
    
    // GJQP
    [12, 15], [15, 6], [6, 5], [5, 12],
    
    // JGIL
    [15, 12], [12, 13], [13, 14], [14, 15],
    
    // QKECMOLJ
    [6, 7], [7, 8], [8, 9], [9, 2], [2, 3], [3, 14], [14, 15], [15, 6],
    
    // BAFDNPGI
    [1, 0], [0, 11], [11, 10], [10, 4], [4, 5], [5, 12], [12, 13], [13, 1],
];


/**
 * Матэматычныя функцыі для працы з вектарамі і матрыцамі
 */

// Аперацыі з вектарамі
const Vector3D = {
    create: function(x, y, z) {
        return [x, y, z];
    },
    
    add: function(v1, v2) {
        return [
            v1[0] + v2[0],
            v1[1] + v2[1],
            v1[2] + v2[2]
        ];
    },
    
    subtract: function(v1, v2) {
        return [
            v1[0] - v2[0],
            v1[1] - v2[1],
            v1[2] - v2[2]
        ];
    },
    
    multiplyScalar: function(v, scalar) {
        return [
            v[0] * scalar,
            v[1] * scalar,
            v[2] * scalar
        ];
    },
    
    dot: function(v1, v2) {
        return v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2];
    },
    
    cross: function(v1, v2) {
        return [
            v1[1] * v2[2] - v1[2] * v2[1],
            v1[2] * v2[0] - v1[0] * v2[2],
            v1[0] * v2[1] - v1[1] * v2[0]
        ];
    },
    
    length: function(v) {
        return Math.sqrt(v[0] * v[0] + v[1] * v[1] + v[2] * v[2]);
    },
    
    normalize: function(v) {
        const len = this.length(v);
        if (len === 0) return [0, 0, 0];
        return [
            v[0] / len,
            v[1] / len,
            v[2] / len
        ];
    }
};

// Аперацыі з матрыцамі 4x4 (для аднародных каардынат)
const Matrix4x4 = {
    identity: function() {
        return [
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ];
    },
    
    // Памножыць дзве матрыцы
    multiply: function(m1, m2) {
        const result = [[0,0,0,0], [0,0,0,0], [0,0,0,0], [0,0,0,0]];
        
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                for (let k = 0; k < 4; k++) {
                    result[i][j] += m1[i][k] * m2[k][j];
                }
            }
        }
        
        return result;
    },
    
    // Памножыць матрыцу на вектар [x, y, z, 1]
    multiplyVector: function(m, v) {
        // Дадаць аднародную каардынату
        const v4 = [v[0], v[1], v[2], 1];
        const result = [0, 0, 0, 0];
        
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                result[i] += m[i][j] * v4[j];
            }
        }
        
        return [result[0], result[1], result[2]];
    },
    
    // Матрыца маштабавання
    scaling: function(sx, sy, sz) {
        return [
            [sx, 0, 0, 0],
            [0, sy, 0, 0],
            [0, 0, sz, 0],
            [0, 0, 0, 1]
        ];
    },
    
    // Матрыца пераносу
    translation: function(tx, ty, tz) {
        return [
            [1, 0, 0, tx],
            [0, 1, 0, ty],
            [0, 0, 1, tz],
            [0, 0, 0, 1]
        ];
    },
    
    // Матрыца павароту вакол восі X (кут у градусах)
    rotationX: function(angle) {
        const rad = angle * Math.PI / 180;
        const c = Math.cos(rad);
        const s = Math.sin(rad);
        
        return [
            [1, 0, 0, 0],
            [0, c, -s, 0],
            [0, s, c, 0],
            [0, 0, 0, 1]
        ];
    },
    
    // Матрыца павароту вакол восі Y (кут у градусах)
    rotationY: function(angle) {
        const rad = angle * Math.PI / 180;
        const c = Math.cos(rad);
        const s = Math.sin(rad);
        
        return [
            [c, 0, s, 0],
            [0, 1, 0, 0],
            [-s, 0, c, 0],
            [0, 0, 0, 1]
        ];
    },
    
    // Матрыца павароту вакол восі Z (кут у градусах)
    rotationZ: function(angle) {
        const rad = angle * Math.PI / 180;
        const c = Math.cos(rad);
        const s = Math.sin(rad);
        
        return [
            [c, -s, 0, 0],
            [s, c, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ];
    },
    
    // Матрыца павароту вакол адвольнай восі
    rotationAroundAxis: function(axis, angle) {
        const u = Vector3D.normalize(axis);
        const rad = angle * Math.PI / 180;
        const c = Math.cos(rad);
        const s = Math.sin(rad);
        const oneMinusC = 1 - c;
        
        // Формула Родрыга
        return [
            [
                c + u[0]*u[0]*oneMinusC,
                u[0]*u[1]*oneMinusC - u[2]*s,
                u[0]*u[2]*oneMinusC + u[1]*s,
                0
            ],
            [
                u[1]*u[0]*oneMinusC + u[2]*s,
                c + u[1]*u[1]*oneMinusC,
                u[1]*u[2]*oneMinusC - u[0]*s,
                0
            ],
            [
                u[2]*u[0]*oneMinusC - u[1]*s,
                u[2]*u[1]*oneMinusC + u[0]*s,
                c + u[2]*u[2]*oneMinusC,
                0
            ],
            [0, 0, 0, 1]
        ];
    },
    
    // Упарадкаваная матрыца для адлюстравання
    toOrderedString: function(matrix) {
        let result = '';
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                result += matrix[i][j].toFixed(3).padStart(8) + ' ';
            }
            result += '\n';
        }
        return result;
    }
};

window.Letter3D = {
    vertices: letterPVertices,
    faces: letterPFaces,
    edges: letterPEdges,
    Vector3D: Vector3D,
    Matrix4x4: Matrix4x4,
    
    vertexIndices: {
        'A': 0, 'B': 1, 'M': 2, 'O': 3,
        'N': 4, 'P': 5, 'Q': 6, 'K': 7,
        'E': 8, 'C': 9, 'D': 10, 'F': 11,
        'G': 12, 'I': 13, 'L': 14, 'J': 15
    },
    
    getVertexCount: function() {
        return this.vertices.length;
    },
    
    getFaceCount: function() {
        return this.faces.length;
    },
    
    getEdgeCount: function() {
        return this.edges.length;
    },
    
    getCenter: function() {
        if (this.vertices.length === 0) return [0, 0, 0];
        
        let sumX = 0, sumY = 0, sumZ = 0;
        for (const vertex of this.vertices) {
            sumX += vertex[0];
            sumY += vertex[1];
            sumZ += vertex[2];
        }
        
        const count = this.vertices.length;
        return [sumX / count, sumY / count, sumZ / count];
    },
    
    getDescription: function() {
        return "Літара 'П' па зададзеных каардынатах. 16 вяршынь, 10 мнагавугольнікаў.";
    },
    
    getVertexInfo: function(index) {
        const letters = Object.keys(this.vertexIndices);
        for (const letter of letters) {
            if (this.vertexIndices[letter] === index) {
                return `${letter}(${this.vertices[index][0]}, ${this.vertices[index][1]}, ${this.vertices[index][2]})`;
            }
        }
        return `Вяршыня ${index}`;
    }
};

window.Letter3D = {
    vertices: letterPVertices,
    faces: letterPFaces,
    edges: letterPEdges,
    Vector3D: Vector3D,
    Matrix4x4: Matrix4x4,
    
    // Індэксы для зручнасці
    vertexIndices: {
        'A': 0, 'B': 1, 'M': 2, 'O': 3,
        'N': 4, 'P': 5, 'Q': 6, 'K': 7,
        'E': 8, 'C': 9, 'D': 10, 'F': 11,
        'G': 12, 'I': 13, 'L': 14, 'J': 15
    },
    
    getRotatedVertices: function() {
        const rotationMatrix = this.Matrix4x4.rotationX(-90);
        
        return this.vertices.map(vertex => {
            return this.Matrix4x4.multiplyVector(rotationMatrix, vertex);
        });
    },
    
    getUprightVertices: function() {
        return [
            // Задняя плоскасць (y = -3)
            [0.5, -3, 0],    // 0: A - было [0.5, 1, 0]
            [1.5, -3, 0],    // 1: B - было [1.5, 1, 0]
            [0.5, -3, 0],    // 2: M - было [0.5, -1, 0] 
            [1.5, -3, 0],    // 3: O - было [1.5, -1, 0]
            
            [-0.5, -3, 0],   // 4: N - было [-0.5, 1, 0]
            [-1.5, -3, 0],   // 5: P - было [-1.5, 1, 0]
            [-1.5, -3, 0],   // 6: Q - было [-1.5, -1, 0]
            [-0.5, -3, 0],   // 7: K - было [-0.5, -1, 0]
            
            // Пярэдняя плоскасць (y = 1-2)
            [-0.5, 1, 0],    // 8: E - было [-0.5, -1, 4]
            [0.5, 1, 0],     // 9: C - было [0.5, -1, 4]
            [-0.5, 1, 0],    // 10: D - было [-0.5, 1, 4]
            [0.5, 1, 0],     // 11: F - было [0.5, 1, 4]
            
            [-1.5, 2, 0],    // 12: G - было [-1.5, 1, 5]
            [1.5, 2, 0],     // 13: I - было [1.5, 1, 5]
            [1.5, 2, 0],     // 14: L - было [1.5, -1, 5]
            [-1.5, 2, 0]     // 15: J - было [-1.5, -1, 5]
        ];
    },
    
    getVertexCount: function() {
        return this.vertices.length;
    },
    
    getFaceCount: function() {
        return this.faces.length;
    },
    
    getEdgeCount: function() {
        return this.edges.length;
    },
    
    getCenter: function() {
        if (this.vertices.length === 0) return [0, 0, 0];
        
        let sumX = 0, sumY = 0, sumZ = 0;
        for (const vertex of this.vertices) {
            sumX += vertex[0];
            sumY += vertex[1];
            sumZ += vertex[2];
        }
        
        const count = this.vertices.length;
        return [sumX / count, sumY / count, sumZ / count];
    },
    
    getDescription: function() {
        return "Літара 'П' стаіць прама (вертыкальна). 16 вяршынь, 10 мнагавугольнікаў.";
    },
    
    // Функцыя для атрымання інфармацыі пра вяршыню
    getVertexInfo: function(index) {
        const letters = Object.keys(this.vertexIndices);
        for (const letter of letters) {
            if (this.vertexIndices[letter] === index) {
                return `${letter}(${this.vertices[index][0]}, ${this.vertices[index][1]}, ${this.vertices[index][2]})`;
            }
        }
        return `Вяршыня ${index}`;
    }
};