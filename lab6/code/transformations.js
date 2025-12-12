
class Transformations3D {
     constructor() {

        this.scale = { x: 1, y: 1, z: 1 };
        this.translate = { x: 0, y: 0, z: 0 };
        this.rotate = { x: 0, y: 0, z: 0 };
        
        this.customAxis = { x: 1, y: 1, z: 1 };
        this.customAngle = 0;
        
        this.transformationMatrix = window.Letter3D.Matrix4x4.identity();
        
        this.originalVertices = window.Letter3D.vertices.map(v => [...v]);
        this.transformedVertices = [...this.originalVertices];
        
        this.viewRotation = { x: 0, y: 0, z: 0 };
    }

    updateTransformationMatrix() {
        let matrix = window.Letter3D.Matrix4x4.identity();
        
        const scaleMatrix = window.Letter3D.Matrix4x4.scaling(
            this.scale.x,
            this.scale.y,
            this.scale.z
        );
        matrix = window.Letter3D.Matrix4x4.multiply(matrix, scaleMatrix);
        
        if (this.rotate.x !== 0) {
            const rotXMatrix = window.Letter3D.Matrix4x4.rotationX(this.rotate.x);
            matrix = window.Letter3D.Matrix4x4.multiply(matrix, rotXMatrix);
        }
        
        if (this.rotate.y !== 0) {
            const rotYMatrix = window.Letter3D.Matrix4x4.rotationY(this.rotate.y);
            matrix = window.Letter3D.Matrix4x4.multiply(matrix, rotYMatrix);
        }
        
        if (this.rotate.z !== 0) {
            const rotZMatrix = window.Letter3D.Matrix4x4.rotationZ(this.rotate.z);
            matrix = window.Letter3D.Matrix4x4.multiply(matrix, rotZMatrix);
        }
        
        if (this.customAngle !== 0) {
            const axis = [this.customAxis.x, this.customAxis.y, this.customAxis.z];
            const customRotMatrix = window.Letter3D.Matrix4x4.rotationAroundAxis(axis, this.customAngle);
            matrix = window.Letter3D.Matrix4x4.multiply(matrix, customRotMatrix);
        }
        
        const translateMatrix = window.Letter3D.Matrix4x4.translation(
            this.translate.x,
            this.translate.y,
            this.translate.z
        );
        matrix = window.Letter3D.Matrix4x4.multiply(matrix, translateMatrix);
        
        const viewRotX = window.Letter3D.Matrix4x4.rotationX(this.viewRotation.x);
        const viewRotY = window.Letter3D.Matrix4x4.rotationY(this.viewRotation.y);
        const viewRotZ = window.Letter3D.Matrix4x4.rotationZ(this.viewRotation.z);
        
        let viewMatrix = window.Letter3D.Matrix4x4.multiply(viewRotY, viewRotX);
        viewMatrix = window.Letter3D.Matrix4x4.multiply(viewMatrix, viewRotZ);
        
        matrix = window.Letter3D.Matrix4x4.multiply(matrix, viewMatrix);
        
        this.transformationMatrix = matrix;
        return matrix;
    }           
    
    applyTransformations(vertices) {
        this.updateTransformationMatrix();
        
        // Пераўтварыць усе вяршыні
        this.transformedVertices = vertices.map(vertex => {
            return window.Letter3D.Matrix4x4.multiplyVector(this.transformationMatrix, vertex);
        });
        
        return this.transformedVertices;
    }
    
    getProjections(vertices, plane) {
    const projected = [];
    
    switch (plane) {
        case 'xy':
            for (const v of vertices) {
                projected.push([v[0], v[1]]); 
            }
            break;
            
        case 'xz':
            for (const v of vertices) {
                projected.push([v[0], v[2]]);
            }
            break;
            
        case 'yz':
            for (const v of vertices) {
                projected.push([v[1], v[2]]); 
            }
            break;
    }
    
    return projected;
}
    
    resetAll() {
        this.scale = { x: 1, y: 1, z: 1 };
        this.translate = { x: 0, y: 0, z: 0 };
        this.rotate = { x: 0, y: 0, z: 0 };
        this.customAngle = 0;
        this.customAxis = { x: 1, y: 1, z: 1 };
        this.viewRotation = { x: 0, y: 0, z: 0 };
        this.transformationMatrix = window.Letter3D.Matrix4x4.identity();
    }
    
    resetScale() {
        this.scale = { x: 1, y: 1, z: 1 };
    }
    
    resetTranslate() {
        this.translate = { x: 0, y: 0, z: 0 };
    }
    
    resetRotation() {
        this.rotate = { x: 0, y: 0, z: 0 };
        this.customAngle = 0;
    }
    
    getMatrixString() {
        const m = this.transformationMatrix;
        let result = '';
        
        for (let i = 0; i < 4; i++) {
            for (let j = 0; j < 4; j++) {
                result += m[i][j].toFixed(3).padStart(8) + ' ';
            }
            result += '\n';
        }
        
        return result;
    }
    
    setScale(x, y, z) {
        this.scale.x = x;
        this.scale.y = y;
        this.scale.z = z;
    }
    
    setTranslate(x, y, z) {
        this.translate.x = x;
        this.translate.y = y;
        this.translate.z = z;
    }
    
    setRotate(x, y, z) {
        this.rotate.x = x;
        this.rotate.y = y;
        this.rotate.z = z;
    }
    
    setViewRotation(x, y, z) {
        this.viewRotation.x = x;
        this.viewRotation.y = y;
        this.viewRotation.z = z;
    }
    
    setCustomRotation(axis, angle) {
        this.customAxis = { x: axis[0], y: axis[1], z: axis[2] };
        this.customAngle = angle;
    }
}

window.Transformations3D = Transformations3D;