package main

import (
	"time"

	"github.com/gin-gonic/gin"
)

func main() {
	router := gin.Default()

	router.GET("/rates", ratesHandler(0))
	router.GET("/rates_null", ratesHandler(3))
	router.POST("/prices", pricesHandler)

	router.Run()
	// router.Run(":3000") // or some configured port
}

// rates_handler = create_rates_handler(
// 	orig_ports_param,
// 	dest_ports_param,
// 	fetch_rates
// )

// PeriodQueryParam wrapp period data from requests
type PeriodQueryParam struct {
	From time.Time `form:"date_from" binding:"required" time_format:"2006-01-02"`
	To   time.Time `form:"date_to" binding:"required" time_format:"2006-01-02"`
}

func ratesHandler(minSample int) func(c *gin.Context) {
	return func(c *gin.Context) {
		var period PeriodQueryParam
		if err := c.ShouldBindQuery(&period); err != nil {
			c.JSON(400, gin.H{"error": err.Error()})
			return
		}

		c.JSON(200, gin.H{
			"message": "rates" + string(minSample),
			"from":    period.From,
			"to":      period.To,
		})
	}
}

func pricesHandler(c *gin.Context) {
	c.JSON(200, gin.H{
		"message": "prices",
	})
}
