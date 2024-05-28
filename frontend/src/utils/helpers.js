// Function to convert datetime string to a more human-readable format
export function convertDatetime(datetime_str) {
    let dateObj = new Date(datetime_str);

    // Get the year, month, and day
    let year = dateObj.getFullYear();
    let month = dateObj.getMonth() + 1;  // getMonth() returns a 0-based value (0=January, 11=December)
    let day = dateObj.getDate();
    let hours = dateObj.getHours();
    let minutes = dateObj.getMinutes();

    // Pad the month and day with leading zeros if necessary
    month = month < 10 ? '0' + month : month;
    day = day < 10 ? '0' + day : day;
    hours = hours < 10 ? '0' + hours : hours;
    minutes = minutes < 10 ? '0' + minutes : minutes;
    
    // Format the date in the 'YYYY/MM/DD' format
    let readableDate = `${day}/${month}/${year} ${hours}:${minutes}`;

    return readableDate;
}