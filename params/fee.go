package params

// Fee holds price and currency params used in the API's
type Fee struct {
	Price    float64 `json:"price" binding:"required"`
	Currency string  `json:"currency" binding:"required,len=3"`
}
