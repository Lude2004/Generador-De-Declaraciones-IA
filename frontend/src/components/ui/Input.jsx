 Input({
    name,
    type,
    value,
    onChange,
    onBlue,
    placeholder,
    error,
    success,
    icon
}) {
    return (
        <div className="input-with-icon">
            <input 
                name={name}
                type={type}
                value={value}
                onChange={onChange}
                onBlur={onBlue}
                placeholder={placeholder}
            />
        </div>
    )
}

export default Input