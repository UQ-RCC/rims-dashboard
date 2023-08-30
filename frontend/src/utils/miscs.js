var miscs = {
    roundToTwo(num) {
        if(num)
            return +(Math.round(num + "e+2")  + "e-2");
        else
            return num;
    },

    convertFormattedStrToBytes(fomattedStr) {
        let str = fomattedStr.trim()
        let value = 0
        switch(str.charAt(str.length-1)) {
            case 'K':
                value = 1024 * parseFloat(str.slice(0, -1))
                break
            case 'M':
                value = 1024 * 1024 * parseFloat(str.slice(0, -1))
                break
            case 'G':
                value = 1024 * 1024 * 1024 * parseFloat(str.slice(0, -1))
                break
            case 'T':
                value = 1024 * 1024 * 1024 * 1024 * parseFloat(str.slice(0, -1))
                break
            default:
                value = parseFloat(str)
        }
        return value
    },

    humanFileSize(bytes, si=false, dp=1) {
        const thresh = si ? 1000 : 1024;
    
        if (Math.abs(bytes) < thresh) {
            return bytes + ' B';
        }
    
        const units = si 
            ? ['kB', 'MB', 'GB', 'TB', 'PB', 'EB', 'ZB', 'YB'] 
            : ['KiB', 'MiB', 'GiB', 'TiB', 'PiB', 'EiB', 'ZiB', 'YiB'];
        let u = -1;
        const r = 10**dp;
    
        do {
            bytes /= thresh;
            ++u;
        } while (Math.round(Math.abs(bytes) * r) / r >= thresh && u < units.length - 1);
    
        return bytes.toFixed(dp) + ' ' + units[u];
    }
    ,      
    // maximum memory
    maxMemSize() {
        380 *  1024 * 1024 * 1024
    }
}



export default miscs
