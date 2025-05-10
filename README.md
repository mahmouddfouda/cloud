# cloud


*Also see the included `architecture.png` for the visual version.*

---

## How It Works

1. An order message is published to **SNS Topic** (OrderTopic).
2. SNS forwards the message to **SQS Queue** (`OrderQueue`).
3. **AWS Lambda** consumes the message from SQS, parses it, and stores it in **DynamoDB**.
4. If the Lambda fails 3 times, the message is routed to a **Dead-Letter Queue (DLQ)** for review.

---

## AWS Components

- **DynamoDB Table**: `Orders`
  - Partition Key: `orderId`
  - Attributes: `userId`, `itemName`, `quantity`, `status`, `timestamp`
  
- **SNS Topic**: `OrderTopic`
- **SQS Queue**: `OrderQueue` (with DLQ)
- **Lambda Function**: `OrderProcessor` (Python 3.12)

---

## 📥 Setup Instructions

1. **Create DynamoDB Table**
   - Name: `Orders`
   - Partition Key: `orderId` (String)

2. **Create SNS Topic**
   - Name: `OrderTopic`

3. **Create SQS Queue**
   - Name: `OrderQueue`
   - Configure DLQ with `maxReceiveCount = 3`

4. **Subscribe SQS to SNS**
   - SNS → Subscriptions → Create
   - Protocol: `Amazon SQS`
   - Endpoint: SQS ARN
   - **Update SQS Access Policy** to allow SNS

5. **Create Lambda Function**
   - Runtime: Python 3.12
   - Environment Variable: `TABLE_NAME=Orders`
   - Trigger: `OrderQueue`
   - IAM Role: Allow `dynamodb:PutItem`, `sqs:ReceiveMessage`

---

## Testing

- Go to SNS → Publish Message
- Use this JSON:
```json
{
  "orderId": "O1234",
  "userId": "U123",
  "itemName": "Laptop",
  "quantity": 1,
  "status": "new",
  "timestamp": "2025-05-03T12:00:00Z"
}
