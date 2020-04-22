package main

import (
	"github.com/gin-gonic/gin"
	"github.com/gin-gonic/gin/binding"

	"github.com/felipeguilhermefs/rates/params"
)

func main() {
	router := gin.Default()

	router.GET("/rates", ratesHandler(0))
	router.GET("/rates_null", ratesHandler(3))
	router.POST("/prices", pricesHandler)

	router.Run()
	// router.Run(":3000") // or some configured port
}

// PORT_PATTERN = re.compile(r'^[A-Z]{5}$')
// REGION_PATTERN = re.compile(r'^\w+$')

func ratesHandler(minSample int) func(c *gin.Context) {
	return func(c *gin.Context) {
		var period params.Period
		if err := c.ShouldBindQuery(&period); err != nil {
			c.JSON(400, gin.H{"error": err.Error()})
			return
		}

		var route params.Route
		if err := c.ShouldBindQuery(&route); err != nil {
			c.JSON(400, gin.H{"error": err.Error()})
			return
		}

		c.JSON(200, gin.H{
			"message":     "rates" + string(minSample),
			"from":        period.From,
			"to":          period.To,
			"origin":      route.Origin,
			"destination": route.Destination,
		})
	}
}

func pricesHandler(c *gin.Context) {
	var period params.Period
	if err := c.ShouldBindBodyWith(&period, binding.JSON); err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}

	var route params.Route
	if err := c.ShouldBindBodyWith(&route, binding.JSON); err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}

	var fee params.Fee
	if err := c.ShouldBindBodyWith(&fee, binding.JSON); err != nil {
		c.JSON(400, gin.H{"error": err.Error()})
		return
	}

	c.JSON(200, gin.H{
		"message":     "prices",
		"from":        period.From,
		"to":          period.To,
		"origin":      route.Origin,
		"destination": route.Destination,
		"price":       fee.Price,
		"currency":    fee.Currency,
	})
}
