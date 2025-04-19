export const toSnakeCase = (obj) => {
    if (Array.isArray(obj)) {
        return obj.map(item => toSnakeCase(item));
    } else if (typeof obj === 'object' && obj !== null) {
        const newObj = {};
        for (const key in obj) {
            if (Object.prototype.hasOwnProperty.call(obj, key)) {
                const newKey = key.replace(/([A-Z])/g, (match) => `_${match.toLowerCase()}`);
                newObj[newKey] = toSnakeCase(obj[key]);
            }
        }
        return newObj;
    }
    return obj;
};
