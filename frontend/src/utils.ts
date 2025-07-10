export function formatDatetime (datetime: string) {
  const date = new Date(datetime)
  const formattedDate = date.toLocaleDateString('en-US')
  const formattedTime = date.toLocaleTimeString('en-US')
  return `${formattedDate} ${formattedTime}`
}
