# JDBC/JDBCTemplate Batch Operation
[Link to question](https://stackoverflow.com/questions/13582806/jdbc-jdbctemplate-batch-operation)
**Creation Date:** 1354014208
**Score:** 0
**Tags:** sql, jdbc, batch-processing, jdbctemplate
## Question Body
<p>There are many examples out there with batch insert query using JDBC or JDBCTemplate. </p>

<p>I would like to do a batch sql operation comprises of Select, Insert and Delete. For instance, I need to issue following sql operation in single connection to database. </p>

<ol>
<li>Multiple select (4 queries to different tables) </li>
<li>Multiple insert (4 queries to different tables)</li>
<li>Multiple delete (4 queries to different tables)</li>
</ol>

<p>Does the JDBC or JDBCTemplate supports that? </p>

<p>EDIT Question: </p>

<pre><code>TicketServiceEnforce ticketDao = TicketServiceEnforceImpl.Factory.getInstance();

        // ================================ SELECT ================================
        if (unknownTicketId &gt; ZERO) {
            unknownTicketList = ticketDao.selectUnknownTicket(unknownTicketId);
            if (!unknownTicketList.isEmpty()) {
                attachmentList = ticketDao.selectAttachment(QueryString.SELECT_UNKNOWN_TICKET_ATTACHMENT_BY_ID.toString(), unknownTicketId);
                ticketCodeList = ticketDao.selectTicketCode(QueryString.SELECT_UNKNOWN_TICKET_CODE_BY_ID.toString(), unknownTicketId);
                ticketCommentList = ticketDao.selectComment(QueryString.SELECT_UNKNOWN_TICKET_COMMENT_BY_ID.toString(), unknownTicketId);
            }
        }
        // ================================ INSERT ================================
        // Retrieve customer_id
        if (!unknownTicketList.isEmpty()) {
            // Just display all customers's name in UI
            customerId = ticketDao.selectCustomerIdByName(genericTicket.getCustomerName());

            genericTicket.setCustomerId(customerId);
            genericTicket.setSubject(unknownTicketList.get(ZERO).getSubject());
            genericTicket.setDetails(unknownTicketList.get(ZERO).getDetails());
            genericTicket.setCreationDate(unknownTicketList.get(ZERO).getCreationDate());

            // =====================================================================
            ticketId = ticketDao.createTicket(genericTicket);
            if (ticketId &gt; ZERO) {

                if (!attachmentList.isEmpty()) {
                    ticketDao.createTicketAttachment(ticketId, attachmentList);
                }

                /*
                 * Insert new ticket code
                */
                newTicketCode = generateTicketCode(ticketId);
                if (!ticketCodeList.isEmpty()) {
                    oldTicketCode = ticketCodeList.get(ZERO);

                    ticketDao.createTicketCode(ticketId, newTicketCode);
                }

                /* Insert old unknown ticket code into ticket_email_mapping
                 * This table used to identify the parent child ticket from email - unknown_ticket
                 * by using two queries
                 * 
                 * 1. Select ticket code - select ticket code from ticket_email_mapping using id  
                 * 2. Select ticket id that has previous ticket code - Select id from ticket_email_mapping tem where tem. 
                 * 
                 */
                if (oldTicketCode != null) {
                    String from_sender = null;
                    if (unknownTicketList.size() &gt; ZERO) {
                        from_sender = unknownTicketList.get(ZERO).getFrom();
                    }

                    ticketDao.createTicketEmailMapping(ticketId, oldTicketCode, from_sender);
                }

                if (!ticketCommentList.isEmpty()) {
                    for (GenericTicketComment comment : ticketCommentList) {
                        comment.setTicketId(ticketId);
                    }

                    ticketDao.createTicketComment(QueryString.INSERT_TICKET_COMMENT.toString(), ticketCommentList);
                }

                if (genericTicket.getAssigneeName() != null) {
                    int assigneeId = -1;
                    String firstName = "";
                    TicketAssignee assignee = new TicketAssignee();

                    firstName = genericTicket.getAssigneeName();
                    assigneeId = ticketDao.selectUserId(firstName);

                    assignee.setTicketId(ticketId);
                    assignee.setAssigneeId(assigneeId);

                    ticketDao.createTicketAssignee(assignee);
                }

                // If all successfull
                ticketCreationSuccessful = true;
            }
        }

        // ================================ DELETE ================================
        if (ticketCreationSuccessful) {
            if (!attachmentList.isEmpty()) {
                affectedRow = ticketDao.removeUnknownTicket(QueryString.DELETE_UNKNOWN_TICKET_ATTACHMENT_BY_ID.toString(), unknownTicketId);
            }

            if (!ticketCommentList.isEmpty()) {
                affectedRow = ticketDao.removeUnknownTicket(QueryString.DELETE_UNKNOWN_TICKET_COMMENT_BY_ID.toString(), unknownTicketId);
            }

            affectedRow = ticketDao.removeUnknownTicket(QueryString.DELETE_UNKNOWN_TICKET_CODE_BY_ID.toString(), unknownTicketId);
            affectedRow = ticketDao.removeUnknownTicket(QueryString.DELETE_UNKNOWN_TICKET_BY_ID.toString(), unknownTicketId);
        }
</code></pre>

<p>This is the DAO using normal query operation. Is it possible to rewrite it in store procedure or bulk operation. </p>

<p>Thanks. Please help. </p>

## Answers
### Answer ID: 13833031
<p>As the name says <code>jdbcTemplate.batchUpdate</code> you cannot do select in the batch operations. If you want to do all the operation in one go, just create one big SQL achieving your logic and use <code>JdbcTemplate.#execute(java.lang.String)</code> method.</p>

